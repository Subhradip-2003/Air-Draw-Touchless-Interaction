import cv2
import numpy as np
import mediapipe as mp
import time


class HandCalculator:
    def __init__(self):
        # Video Capture
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        # Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.85, min_tracking_confidence=0.5)
        self.mp_draw = mp.solutions.drawing_utils
        self.last_delete_time = 0
        self.delete_cooldown = 2.0 # seconds (you can adjust this to be faster/slower)

        self.expression = ""
        self.result = None
        self.last_confirm_time = 0
        self.current_display = None
        self.awaiting_confirmation = False

        self.box1 = (50, 200, 400, 600)
        self.box2 = (450, 200, 800, 600)
        self.box3 = (850, 200, 1250, 600)

        self.operator_positions = {
            "R": (50, 20, 150, 70),
            "+": (200, 20, 300, 70),
            "-": (350, 20, 450, 70),
            "*": (500, 20, 600, 70),
            "/": (650, 20, 750, 70),
            "Del": (800, 20, 950, 70),   # <<<<<<---- added Delete button here
        }

    def draw_ui(self, img):
        """Draws the input boxes and operator buttons."""
        cv2.rectangle(img, (self.box1[0], self.box1[1]), (self.box1[2], self.box1[3]), (255, 0, 0), 2)
        cv2.rectangle(img, (self.box2[0], self.box2[1]), (self.box2[2], self.box2[3]), (255, 0, 0), 2)
        cv2.rectangle(img, (self.box3[0], self.box3[1]), (self.box3[2], self.box3[3]), (0, 255, 0), 2)
        cv2.putText(img, "Input 1", (self.box1[0], self.box1[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        cv2.putText(img, "Input 2", (self.box2[0], self.box2[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        cv2.putText(img, "Confirm (Fist)", (self.box3[0], self.box3[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        for op, (x1, y1, x2, y2) in self.operator_positions.items():
            if op == 'R':
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), -1)
            elif op == 'Del':
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 165, 255), -1)  # Orange for Delete
            else:
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), -1)

            cv2.putText(img, op, (x1 + 20, y1 + 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    def count_fingers(self, lm_list, box, left: bool):
        """Counts fingers in a given box and returns a digit."""
        if not lm_list:
            return None

        wrist_x, wrist_y = lm_list[0][1], lm_list[0][2]
        if not (box[0] <= wrist_x <= box[2] and box[1] <= wrist_y <= box[3]):
            return None

        finger_tips = [4, 8, 12, 16, 20]
        finger_pips = [3, 6, 10, 14, 18]
        count = 0

        if left:
            if lm_list[finger_tips[0]][1] > lm_list[finger_pips[0]][1]:
                count += 1
        if not left:
            if lm_list[finger_tips[0]][1] < lm_list[finger_pips[0]][1]:
                count += 1

        for tip, pip in zip(finger_tips[1:], finger_pips[1:]):
            if lm_list[tip][2] < lm_list[pip][2]:
                count += 1

        return min(count, 9)

    def detect_operator_selection(self, lm_list):
        """Detects if the index finger is pointing at an operator button."""
        if not lm_list:
            return None

        index_x, index_y = lm_list[8][1], lm_list[8][2]
        for op, (x1, y1, x2, y2) in self.operator_positions.items():
            if x1 <= index_x <= x2 and y1 <= index_y <= y2:
                return op
        return None

    def evaluate_expression(self):
        """Evaluates the current expression and updates result."""
        try:
            self.result = eval(self.expression, {"__builtins__": {}}, {})
        except Exception:
            self.result = "Error"

    def run(self):
        """Main loop of the calculator."""
        while True:
            ret, img = self.cap.read()
            if not ret:
                print("Failed to grab frame")
                break
            img = cv2.flip(img, 1)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            results_hand = self.hands.process(img_rgb)

            self.draw_ui(img)
            current_time = time.time()

            detected_digit = None
            total_digit = 0
            detected_operator = None
            confirm = False
            both_fists = 0

            if results_hand.multi_hand_landmarks:
                hands_list = []
                for hand_landmarks in results_hand.multi_hand_landmarks:
                    lm_list = [[id, int(lm.x * 1280), int(lm.y * 720)] for id, lm in enumerate(hand_landmarks.landmark)]
                    hands_list.append((lm_list[0][1], lm_list))

                hands_list.sort()

                for idx, (_, lm_list) in enumerate(hands_list):
                    self.mp_draw.draw_landmarks(img, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                    if idx == 0:
                        detected_digit = self.count_fingers(lm_list, self.box1, left=True)
                        if detected_digit is not None:
                            total_digit = detected_digit
                            self.current_display = str(total_digit)
                            if detected_digit == 0:
                                both_fists += 1

                        selected_operator = self.detect_operator_selection(lm_list)
                        if selected_operator:
                            self.current_display = selected_operator
                            if selected_operator == 'R':
                                self.expression = ""
                                self.result = None
                                self.current_display = None
                            elif selected_operator == 'Del' and self.expression:
                                if current_time - self.last_delete_time > self.delete_cooldown:
                                    self.expression = self.expression[:-1]
                                    self.current_display = None  # Don't show 'Del'
                                    self.last_delete_time = current_time

                    elif idx == 1:
                        detected_digit = self.count_fingers(lm_list, self.box2, left=False)
                        if detected_digit is not None:
                            total_digit += detected_digit
                            self.current_display = str(total_digit)
                        elif total_digit is None:
                            total_digit = 0

                for _, lm_list in hands_list:
                    confirm_count = self.count_fingers(lm_list, self.box3, left=False)
                    if confirm_count == 5:
                        confirm = True
                    elif confirm_count == 0:
                        both_fists += 1

            if confirm and self.current_display is not None and not self.awaiting_confirmation:
                self.expression += self.current_display
                self.awaiting_confirmation = True
                self.last_confirm_time = current_time
                self.current_display = None

            if not confirm and self.awaiting_confirmation:
                self.awaiting_confirmation = False

            if both_fists >= 2 and (current_time - self.last_confirm_time > 2):
                self.evaluate_expression()
                self.last_confirm_time = current_time

            # --- Expression part (top-left) ---
            display_text = f"Expression: {self.expression}" if not self.result else f"{self.expression} = {self.result}"
            (text_width, text_height), _ = cv2.getTextSize(display_text, cv2.FONT_HERSHEY_SIMPLEX, 1, 3)
            cv2.rectangle(img, (48, 110), (48 + text_width + 10, 110 + text_height + 20), (255, 255, 255), -1)  # white bg
            cv2.putText(img, display_text, (55, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

# --- Current part (top-right) ---
            if self.current_display:
                current_text = f"Current: {self.current_display}"
                (curr_width, curr_height), _ = cv2.getTextSize(current_text, cv2.FONT_HERSHEY_SIMPLEX, 1, 3)
                cv2.rectangle(img, (890, 110), (890 + curr_width + 10, 110 + curr_height + 20), (255, 255, 255), -1)  # white bg
                cv2.putText(img, current_text, (900, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)


            if self.current_display:
                cv2.putText(img, f"Current: {self.current_display}", (900, 150), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 0, 255), 3)

            cv2.imshow('Hand Calculator', img)
            key = cv2.waitKey(1)
            if key & 0xFF == ord('q'):
                break
            elif key & 0xFF == ord('r'):
                self.expression = ""
                self.result = None
                self.current_display = None

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    HandCalculator().run()
