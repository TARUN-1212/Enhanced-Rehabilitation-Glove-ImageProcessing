# 🖐️ Enhanced Rehabilitation Glove System
> 💡 A computer-vision-based rehabilitation glove designed for stroke survivors and hand injury patients.


Abstract

The Enhanced Rehabilitation System for Hand Injury Patients presents a novel approach to assist individuals recovering from hand injuries or strokes through tailored exercises aimed at expediting their rehabilitation process. This system integrates advanced technologies to facilitate patient recovery more efficiently and engagingly.
Central to the system is the utilization of computer vision technology, which replaces traditional flex sensor-based models. By employing Python for implementation, the system enables real-time customization of exercises based on patient needs and progress. Through a camera interface, healthcare professionals guide patients in performing exercises tailored to their specific condition.
A robotic arm, controlled by an Arduino Uno microcontroller, translates the movements captured by the computer vision system into corresponding actions. Individual servo motors are employed to precisely control hand movements, providing targeted rehabilitation exercises.
This innovative approach offers a more interactive and effective rehabilitation experience for hand injury patients, potentially enhancing their recovery outcomes while reducing reliance on conventional methods.



## 📜 Project Description

The **Enhanced Rehabilitation Glove System** offers a novel approach to support individuals recovering from hand injuries or neurological impairments. Unlike traditional flex sensor-based gloves, this system uses **computer vision (MediaPipe + OpenCV)** to detect hand gestures and control a **robotic glove via Arduino** and **servo motors** for precise movement replication.

This innovative solution allows **customized exercises**, real-time feedback, and **remote interaction** between therapists and patients — making physical therapy more accessible, engaging, and effective.

---

## 🧠 Tech Stack Used

| Technology     | Purpose                          |
|----------------|----------------------------------|
| Python         | Main control and gesture logic   |
| OpenCV         | Video feed and image processing  |
| MediaPipe      | Real-time hand tracking          |
| Tkinter        | GUI for exercise interaction     |
| Arduino (C++)  | Controls servo motors            |
| USB Serial     | Communication between PC and MCU |
| Servo Motors   | Finger movement actuation        |

---

## 💡 How It Works

1. **Gesture Detection (Python + MediaPipe)**  
   Detects the finger positions and classifies open/closed fingers based on key landmark positions.

2. **GUI Interface (Tkinter)**  
   Displays current status and options for different exercises.

3. **Robotic Actuation (Arduino)**  
   Translates detected gestures into servo commands that move each finger accordingly.

4. **Hardware Integration**  
   The glove has embedded servo motors to replicate finger movement for therapy.

---

## 🔧 How to Run the Code

### 🖥️ Prerequisites
Make sure the following are installed:
- Python 3.x
- OpenCV: `pip install opencv-python`
- MediaPipe: `pip install mediapipe`
- PySerial: `pip install pyserial`

### ⚙️ Arduino Setup
1. Open `hand_rehab_arduino_control.ino` in Arduino IDE.
2. Upload to your Arduino Uno.
3. Connect 5 servo motors to digital pins as per `schematic_diagram.jpg`.

### 💻 Run the Main App
```bash
python enhanced_rehabilitation_glove_gui.py
