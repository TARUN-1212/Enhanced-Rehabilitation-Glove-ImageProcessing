import cv2
import mediapipe as mp
# from cvzone.SerialModule import SerialObject  # Uncomment this if using Arduino communication via serial

# Initialize MediaPipe Hand module
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Configure hand detection settings
hands = mp_hands.Hands(
    static_image_mode=False,            # Use video stream (dynamic images)
    max_num_hands=1,                    # Detect only one hand
    min_detection_confidence=0.7,       # Minimum confidence for initial detection
    min_tracking_confidence=0.5         # Minimum confidence for tracking after detection
)

class Hand_Excerises_Detection:
    """
    This class detects which fingers are raised in the camera feed using MediaPipe Hand landmarks.
    It returns the gesture as a list of 0s and 1s, where 1 indicates a raised finger.
    """

    def find_handgeasures(self, frame):
        """
        Detects hand landmarks and identifies which fingers are raised.

        Args:
            frame (np.array): Input video frame in BGR format.

        Returns:
            results: MediaPipe hand detection results.
            finger_status (list): List of 5 elements indicating the status of each finger:
                                  [Thumb, Index, Middle, Ring, Pinky]
        """

        # Convert BGR image to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the image for hand landmarks
        results = hands.process(rgb_frame)
        
        # Initialize all fingers as not raised
        finger_status = [0, 0, 0, 0, 0]

        # If hand landmarks are detected
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Thumb: Compare X coordinates
                if hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x < \
                   hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x:
                    finger_status[0] = 1  # Thumb is raised

                # Index: Compare Y coordinates (Tip above PIP joint)
                if hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y < \
                   hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y:
                    finger_status[1] = 1

                # Middle finger
                if hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y < \
                   hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y:
                    finger_status[2] = 1

                # Ring finger
                if hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y < \
                   hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y:
                    finger_status[3] = 1

                # Little (Pinky) finger
                if hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y < \
                   hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y:
                    finger_status[4] = 1

                # Debug: Print the current finger status
                print(finger_status)

                # Optional: Send data to Arduino using serial
                # My_Serial.sendData(finger_status)

        return results, finger_status

# Instantiate the gesture detection class (example usage)
Hand_Excerises_Detection()
