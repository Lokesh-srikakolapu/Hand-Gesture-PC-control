import mediapipe as mp
import cv2
import pyautogui
import time
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
    
    # List of tabs to switch between
    tabs = ["Tab 1", "Tab 2", "Tab 3", "Tab 4"]
    
    # Current tab index
    current_tab = 0
    
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                thumb_tip = hand_landmarks.landmark[4]
                thumb_base = hand_landmarks.landmark[2]
                if thumb_tip.x < thumb_base.x and thumb_tip.y < thumb_base.y:
                    # Move to previous tab
                    current_tab = (current_tab - 1) % len(tabs)
                    print("Thumb is moving in the left direction. Switching to", tabs[current_tab])
                    pyautogui.hotkey('alt','shift','tab')
                    time.sleep(2)
                    
                elif thumb_tip.x > thumb_base.x and thumb_tip.y < thumb_base.y:
                    # Move to next tab
                    current_tab = (current_tab + 1) % len(tabs)
                    print("Thumb is moving in the right direction. Switching to", tabs[current_tab])
                    pyautogui.hotkey('alt', 'tab')
                    time.sleep(2)
                    

                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()
