# Air-Draw-Touchless-Interaction
✋ Amazing Hand Gesture Projects with Computer Vision & AI

Welcome to a collection of 3 exciting projects where your **hand becomes the controller**! Using a webcam and computer vision, you can adjust volume, perform calculations, and even compete in drawing — all with simple hand gestures. No keyboard or mouse needed.

This repo is great for:
- Students learning OpenCV and MediaPipe
- Beginners exploring hand tracking
- Developers interested in building AI-powered interactive apps

---

## 📦 Projects Included

| Project | Description |
|--------|-------------|
| 🎚️ **Gesture Volume Control** | Control your system volume using your fingers |
| 🧠 **Hand Gesture Calculator** | Do arithmetic just by showing fingers |
| ✍️ **AI Drawing Judge** | Draw with hand and let Google Gemini AI decide the winner |

---

## 🎚️ 1. Gesture Volume Control

Control your system volume just by **moving your fingers**! It's like having an invisible volume knob.

### 🧠 How it works:
- Uses a webcam to track your **thumb and index finger**
- Measures the **distance** between them
- Converts that into a system volume level
- Shows a volume bar on the screen in real-time

### 🛠️ Tech Used:
- Python
- OpenCV
- NumPy
- A custom `HandTrackingModule`

### ▶️ Getting Started

Install the required packages:

pip install opencv-python numpy pycaw comtypes
Run the script:
python GestureVolumeControl.py


-------------------------------------------------------------------------------------------------------------------------------------------------------------------


🧠 2. Hand Gesture Calculator
This is a touchless calculator. Show numbers with fingers, select math operations by pointing, and calculate by showing two fists!

🔍 What you can do:
Use your left hand for the first number (Input 1)

Use your right hand for the second number (Input 2)

Point to buttons on the screen: +, -, *, /

Show fists with both hands to get the result

Use gestures for Reset and Delete

🧠 Technologies:
Python

OpenCV

MediaPipe for real-time hand tracking

Numpy

▶️ Getting Started
Install the required libraries:

bash
Copy code
pip install opencv-python mediapipe numpy
Run the calculator:

python final_calculator.py

Controls:

Press q to quit

Press r to reset manually (or use the gesture)

💡 Why it's cool:
No buttons, no touch — just gestures

Great project to learn gesture detection logic

Full interactive UI with real-time feedback



-------------------------------------------------------------------------------------------------------------------------------------------------------------------



✍️ 3. AI Drawing Judge – With Google Gemini
This is the most fun one — draw with your hand on two sides of the screen, and let Google Gemini AI pick the better drawing! And you can do anything we can want with your new ideas. 

✏️ What you can do:
Use your index finger to draw

Each side (left and right) is a canvas

When done, use a ✌️ gesture (index + middle fingers) to press "Done"

The drawing is sent to Gemini AI, which picks the winner and explains why

🤖 Technologies:
Streamlit for UI

OpenCV + cvzone for drawing with finger

Google Generative AI API (Gemini 1.5 Flash)

Pillow for image processing

🧪 How to Run
Install the packages:

pip install streamlit opencv-python cvzone numpy pillow google-generativeai
👉 Add your Gemini API key in this line of the script:

python
Copy code
ai_instance = GestureMathAI(api_key="YOUR_API_KEY", ...)
Run the app with:

streamlit run Hand_guesture_final.py
Make sure your webcam is on. Draw something on both sides and let the AI judge!

📂 Folder Structure

📁 Hand-Gesture-Projects
├── GestureVolumeControl.py        # Project 1: Volume control
├── final_calculator.py            # Project 2: Calculator
├── Hand_guesture_final.py         # Project 3: Drawing + AI Judge
└── HandTrackingModule.py          # Shared custom module
🎯 Why These Projects Matter
Great introduction to real-time computer vision

Uses hand gestures to make intuitive user interfaces

Shows how to integrate AI with visual input

Beginner-friendly, fun, and useful for college demos or hackathons

💡 Tips for Best Results
Make sure you have a good webcam and decent lighting

Keep your hand steady and inside the camera frame

Restart the script if tracking fails

Practice makes gestures smoother!

📜 License
These projects are open-sourced under the MIT License. Feel free to use them in your own projects, modify them, or learn from them.

🙌 Thanks To:
MediaPipe – hand tracking

OpenCV – image and video processing

Google Gemini AI – AI text generation

Streamlit – easy-to-use app UI


-------------------------------------------------------------------------------------------------------------------------------------------------------------------


Here is the all three projects . If you any kind of help feel free to ask . 
Email - subhradipbhradipbhattacharyya290@gmail.com
linkdin - www.linkedin.com/in/subhradip2003

Thank you . 
