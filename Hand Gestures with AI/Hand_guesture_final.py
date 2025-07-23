from PIL import Image
import cv2
import numpy as np
import streamlit as st
from cvzone.HandTrackingModule import HandDetector
import google.generativeai as genai

class GestureMathAI:
    def __init__(self, api_key, prompt):
        self.prompt = prompt
        self.canvas = None
        self.previous_position = None
        self.output_text = ""

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

        self.detector = HandDetector(staticMode=False,
                                     maxHands=1,
                                     modelComplexity=1,
                                     detectionCon=0.7,
                                     minTrackCon=0.5)

        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        # Define confirmation button area
        self.confirmation_area = (1100, 50, 1250, 150)  # x1, y1, x2, y2

        self.drawing_confirmed = False

    def get_hands_info(self, frame):
        hands, _ = self.detector.findHands(frame, draw=False, flipType=True)
        if hands:
            return self.detector.fingersUp(hands[0]), hands[0]["lmList"]
        return None

    def draw_on_canvas(self, hand_info):
        fingers, landmarks = hand_info
        current_position = None

        if fingers == [0, 1, 0, 0, 0]:  # Only index finger up (for drawing)
            current_position = landmarks[8][:2]
            if self.previous_position is None:
                self.previous_position = current_position
            cv2.line(self.canvas, tuple(current_position), tuple(self.previous_position), (255, 0, 255), 10)

        elif fingers == [1, 1, 1, 1, 1]:  # All fingers up to reset canvas
            self.canvas = np.zeros_like(self.canvas)
            self.output_text = ""
            self.drawing_confirmed = False  # <-- Reset "Done" status!

        self.previous_position = current_position

    def draw_confirmation_button(self, frame):
        x1, y1, x2, y2 = self.confirmation_area
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, 'Done', (x1 + 20, y1 + 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)

    def check_confirmation(self, hand_info):
        fingers, landmarks = hand_info
        if fingers == [0, 1, 1, 0, 0]:  # Only index and middle finger up
            x, y = landmarks[8][:2]  # Index finger tip position
            x1, y1, x2, y2 = self.confirmation_area
            if x1 < x < x2 and y1 < y < y2:
                return True
        return False

    def send_to_ai(self):
        try:
            pil_image = Image.fromarray(self.canvas)
            response = self.model.generate_content([self.prompt, pil_image])
            return response.text
        except Exception as e:
            return f'Error: {str(e)}'

    def run(self):
        st.set_page_config(layout='wide')
        col1, col2 = st.columns([2, 1])

        with col1:
            run_app = st.checkbox('Run', value=True)
            frame_window = st.image([])

        with col2:
            st.title("Answer")
            output_display = st.subheader("")

        try:
            while run_app:
                ret, frame = self.cap.read()
                if not ret:
                    break
                frame = cv2.flip(frame, 1)
                if self.canvas is None:
                    self.canvas = np.zeros_like(frame)

                hand_info = self.get_hands_info(frame)
                if hand_info:
                    self.draw_on_canvas(hand_info)

                    if self.check_confirmation(hand_info) and not self.drawing_confirmed:
                        self.output_text = self.send_to_ai()
                        self.drawing_confirmed = True  # Confirm only once for current drawing

                # Draw the confirmation button
                self.draw_confirmation_button(frame)

                # Blend the canvas and frame
                blended_image = cv2.addWeighted(frame, 0.7, self.canvas, 0.3, 0)
                frame_window.image(blended_image, channels="BGR")

                if self.output_text:
                    output_display.text(self.output_text)
                else:
                    output_display.text("")

        except Exception as e:
            st.error(f"Error: {str(e)}")
        finally:
            self.cap.release()
            cv2.destroyAllWindows()


if __name__ == "__main__":
    ai_instance = GestureMathAI(api_key="AIzaSyBiECkwy7IgGu5Tri7PpPzV4bq-RoI7GiI", prompt="There will be two drawing partition by one big line . Compare which is best in drawing in the artistic view . If left win write left else right. And give reason why that better")
    ai_instance.run()
