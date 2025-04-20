# Import necessary libraries
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import cv2
import mediapipe as mp
import HandExercise  # Custom module for hand gesture detection
import serial.tools.list_ports
from cvzone.SerialModule import SerialObject  # For Serial communication (Arduino, etc.)

# Initialize the hand detection module from the custom HandExercise module
hand_detector = HandExercise.Hand_Excerises_Detection()

# GUI Class for Camera-based Hand Exercise
class CameraApp:
    def _init_(self, parent):
        self.parent = parent
        self.cam_window = tk.Toplevel(parent)  # Create a separate window for the camera interface
        self.cam_window.geometry("1200x600")
        self.cam_window.title("Camera App")
        self.cam_window.resizable(False, False)
        self.cam_window.configure(bg='#3A7FF6')
        self.imgtk = None  # ImageTk reference to keep the frame persistent

        # Button to connect serial port
        self.connect_button = tk.Button(self.cam_window, width=15, text='Connect port', bg='red', fg='white', command=self.find_available_port)
        self.connect_button.place(x=970, y=40)

        # Define UI Frames for layout
        left_frame = tk.Frame(self.cam_window, bg='#3A7FF6', highlightbackground="white", highlightthickness=2)
        left_frame.place(x=40, y=80, width=270, height=500)

        self.right_frame = tk.Frame(self.cam_window, bg='#3A7FF6', highlightbackground="white", highlightthickness=2)
        self.right_frame.place(x=320, y=80, width=630, height=500)

        self.rest_frame = tk.Frame(self.cam_window, bg='#3A7FF6', highlightbackground="white", highlightthickness=2)
        self.rest_frame.place(x=960, y=80, width=200, height=500)

        # Label to display video feed
        self.camera_label = tk.Label(self.right_frame, text="Camera Label", font=('Arial', 20, 'bold'), fg="white", bg='#3A7FF6')
        self.camera_label.pack()

        # System description label
        self.system_label = tk.Label(self.cam_window, text="With each exercise, you regain your strength", font=('Arial', 20, 'bold'), bg='#3A7FF6', fg='white')
        self.system_label.place(x=300, y=20)

        # Finger status label and text area
        self.finger_status_heading = tk.Label(self.rest_frame, text="Finger Status", font=('Arial', 12, 'bold'), bg='white', fg='#3A7FF6')
        self.finger_status_heading.pack(side="top", fill="x", padx=5, pady=5)

        self.finger_status_text = tk.Text(self.rest_frame, wrap="none")
        self.finger_status_text.pack(side="left", fill="y")

        # Scrollbar for status text
        self.scrollbar = ttk.Scrollbar(self.rest_frame, orient="vertical", command=self.finger_status_text.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.finger_status_text.config(yscrollcommand=self.scrollbar.set)

        # MediaPipe setup
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()

        # Buttons for various functionalities
        self.Live_button = tk.Button(left_frame, width=25, text='Live Exercise', bg='white', fg="#3A7FF6", state='disabled', command=self.start_live_feed)
        self.Live_button.pack(pady=20)

        self.Video_button = tk.Button(left_frame, width=25, text='Recorded Exercises', bg='white', fg="#3A7FF6", state='disabled', command=self.enable_button)
        self.Video_button.pack(pady=20)

        self.v1_button = tk.Button(left_frame, width=25, text='Video 1', bg='white', fg="#3A7FF6", state='disabled', command=self.start_video_feed)
        self.v1_button.pack(pady=20)

        self.v2_button = tk.Button(left_frame, width=25, text='Video 2', bg='white', fg="#3A7FF6", state='disabled')
        self.v2_button.pack(pady=20)

        self.v3_button = tk.Button(left_frame, width=25, text='Video 3', bg='white', fg="#3A7FF6", state='disabled')
        self.v3_button.pack(pady=20)

        self.stop_button = tk.Button(left_frame, width=25, text='Start Exercise', bg='white', fg="black", state='disabled', command=self.stop_camera)
        self.stop_button.pack(pady=20)

        self.exit_button = tk.Button(left_frame, width=25, text='Exit', bg='white', fg="#3A7FF6", command=self.exit_camera)
        self.exit_button.pack(pady=20)

        self.cap = None  # Capture object for video feed

    # Method to search for available COM ports and connect to device
    def find_available_port(self):
        def check():
            available_ports = serial.tools.list_ports.comports()
            for port in available_ports:
                if "COM" in port.device:
                    return port.device
            return None

        port = check()
        if port:
            self.My_Serial = SerialObject(port, 9600, 1)
            messagebox.showinfo("Port Connected", f"Connected to port: {port}", parent=self.cam_window)
            self.Live_button.config(state='normal')
            self.Video_button.config(state='normal')
            self.stop_button.config(state='normal')
            self.connect_button.config(bg='green', text='Port connected')
            self.stop_button.config(bg='green', fg='white')
        else:
            messagebox.showerror("Port Error", "No COM port available. Check your connections.", parent=self.cam_window)
            self.connect_button.config(bg='red', text='Connect Port')

    # Start live camera feed
    def start_live_feed(self):
        self.stop_button.config(text='Stop', bg="red", fg='white')
        if self.cap is not None:
            self.cap.release()
        self.cap = cv2.VideoCapture(0)
        self.display_camera_feed()

    # Start playback from recorded video
    def start_video_feed(self):
        self.stop_button.config(text='Stop', bg="red", fg='white')
        if self.cap is not None:
            self.cap.release()
        video_path = r'C:\Users\2024au\Desktop\Python(3)\EnhancedRehabilitationGloveSystem\videos\hand_test.mp4'
        self.cap = cv2.VideoCapture(video_path)
        self.display_camera_feed()

    # Core method to display frames from camera or video
    def display_camera_feed(self):
        ret, frame_ = self.cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame_, cv2.COLOR_BGR2RGB)
            results, finger_status = hand_detector.find_handgeasures(frame_)  # Use custom module to detect gestures
            self.My_Serial.sendData(finger_status)  # Send data over serial

            # Display finger status in text area
            self.finger_status_text.insert("end", str(finger_status) + "\n")
            self.finger_status_text.see("end")

            # Draw hand landmarks
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.draw_hand_landmarks(frame_rgb, hand_landmarks)

            img = Image.fromarray(frame_rgb).resize((640, 480), Image.LANCZOS)
            self.imgtk = ImageTk.PhotoImage(image=img)
            self.camera_label.imgtk = self.imgtk
            self.camera_label.config(image=self.imgtk)
            self.camera_label.after(10, self.display_camera_feed)

    # Draw landmarks on the frame
    def draw_hand_landmarks(self, frame, landmarks):
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing.draw_landmarks(frame, landmarks, self.mp_hands.HAND_CONNECTIONS)

    # Enable video playback buttons
    def enable_button(self):
        self.v1_button.config(state='normal')
        self.v2_button.config(state='normal')
        self.v3_button.config(state='normal')

    # Stop video/camera feed
    def stop_camera(self):
        if self.cap is not None:
            self.cap.release()
        self.stop_button.config(text='Start Exercise', bg="green", fg='white')
        self.camera_label.config(text="Camera Label", font=('Arial', 20, 'bold'), fg="white", bg='#3A7FF6')

    # Exit the app window
    def exit_camera(self):
        if self.cap is not None:
            self.cap.release()
        self.cam_window.destroy()


# (App class not included fully, you can apply similar comments to the rest of it)

