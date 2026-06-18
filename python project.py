import cv2
import mediapipe as mp
import serial
import time
import pygame  # ✅ for playing sound

# ✅ Setup serial for Arduino — set your correct COM port
try:
    arduino = serial.Serial('COM4', 9600)
    time.sleep(2)
except Exception as e:
    print("⚠️ Serial init failed:", e)
    arduino = None

# ✅ Initialize pygame mixer for sounds
pygame.mixer.init()

# Function to play sound safely
def play_sound(filename):
    try:
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
    except Exception as e:
        print("⚠️ Sound play error:", e)

# Setup MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Capture video
cap = cv2.VideoCapture(0)

# Brightness handling
brightness = 0
target_brightness = 0
gesture_brightness = 255
last_sent = -1
last_seen_time = time.time()
AUTO_OFF_DELAY = 10
DIM_SPEED = 10
person_present = False
hello_played = False

def count_fingers(landmarks, hand_label):
    tips = [4, 8, 12, 16, 20]
    fingers = []
    if hand_label == "Right":
        fingers.append(landmarks.landmark[tips[0]].x < landmarks.landmark[tips[0] - 1].x)
    else:
        fingers.append(landmarks.landmark[tips[0]].x > landmarks.landmark[tips[0] - 1].x)
    for i in range(1, 5):
        fingers.append(landmarks.landmark[tips[i]].y < landmarks.landmark[tips[i] - 2].y)
    return sum(fingers)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    person_detected = len(faces) > 0
    current_time = time.time()
    results = hands.process(rgb)
    gesture_detected = False

    if person_detected:
        # Draw green box around detected person(s)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "Person Detected", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        if not person_present:
            if arduino:
                arduino.write(b"P_ON\n")
                print("👤 Person detected → sent P_ON")
            else:
                print("👤 Person detected (serial not available)")
            play_sound("hello.mp3")  # ✅ Plays when person appears
            hello_played = True

        person_present = True
        last_seen_time = current_time

        # Gesture detection
        if results.multi_hand_landmarks:
            for hand_landmarks, hand_type in zip(results.multi_hand_landmarks, results.multi_handedness):
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                label = hand_type.classification[0].label
                fingers = count_fingers(hand_landmarks, label)

                if fingers == 0:
                    gesture_brightness = 0
                    cv2.putText(frame, "Gesture: 0 Fingers", (10, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                elif fingers == 1:
                    gesture_brightness = 50
                    cv2.putText(frame, "Gesture: 1 Finger", (10, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                elif fingers == 2:
                    gesture_brightness = 127
                    cv2.putText(frame, "Gesture: 2 Fingers", (10, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                elif fingers == 3:
                    gesture_brightness = 180
                    cv2.putText(frame, "Gesture: 3 Fingers", (10, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                elif fingers == 5:
                    gesture_brightness = 255
                    cv2.putText(frame, "Gesture: 5 Fingers", (10, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                else:
                    gesture_brightness = 255

                gesture_detected = True
                break

        target_brightness = gesture_brightness if gesture_detected else gesture_brightness

    else:
        # 🚫 No person detected → after delay, turn off
        if person_present and (current_time - last_seen_time > AUTO_OFF_DELAY):
            if arduino:
                arduino.write(b"P_OFF\n")
                print("🚫 Person gone → sent P_OFF")
            else:
                print("🚫 Person gone (serial not available)")
            play_sound("alert.mp3")  # ✅ Alert sound when no person
            person_present = False
            target_brightness = 0
            hello_played = False

    # Smooth transition for brightness
    if brightness < target_brightness:
        brightness = min(brightness + DIM_SPEED, target_brightness)
    elif brightness > target_brightness:
        brightness = max(brightness - DIM_SPEED, target_brightness)

    # Send brightness only when it changes
    if brightness != last_sent:
        if arduino:
            try:
                arduino.write(f"{brightness}\n".encode())
                print(f"Sent brightness: {brightness}")
                last_sent = brightness
            except Exception as e:
                print("⚠️ Serial write failed:", e)
        else:
            print(f"(No serial) Brightness would be: {brightness}")
            last_sent = brightness

    cv2.putText(frame, f"Brightness: {brightness}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    cv2.imshow("Smart Control", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
arduino.close()
cv2.destroyAllWindows()
