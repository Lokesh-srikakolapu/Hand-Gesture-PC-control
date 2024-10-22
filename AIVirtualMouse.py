import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy
import pyautogui
######################
wCam, hCam = 640, 480
frameR = 100     #Frame Reduction
smoothening = 7  #random value
######################

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()
print(wScr, hScr)

while True:
    # Step1: Find the landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    # Step2: Get the tip of the index and middle finger
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        x4, y4 = lmList[4][1:]
        x5, y5 = lmList[2][1:]
        x6, y6 = lmList[16][1:]
        x7, y7 = lmList[20][1:]
        # Step3: Check which fingers are up
        fingers = detector.fingersUp()
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                      (255, 0, 255), 2)
        tabs = ["Tab 1", "Tab 2", "Tab 3", "Tab 4"]
        current_tab = 0
        if fingers == [1, 0, 0, 0, 0] and x4 < x5 and y4 < y5:
            # Move to previous tab
            current_tab = (current_tab - 1) % len(tabs)
            # print("Thumb is moving in the left direction. Switching to", tabs[current_tab])
            pyautogui.hotkey('alt','shift','tab')
            time.sleep(1)
        # Step4: Only Index Finger: Moving Mode
        if fingers == [0, 1, 0, 0, 0]:

            # Step5: Convert the coordinates
            x3 = np.interp(x1, (frameR, wCam-frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScr))

            # Step6: Smooth Values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            # Step7: Move Mouse
            autopy.mouse.move(wScr - clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY
        # Step8: Both Index and middle are up: Clicking Mode
        if fingers == [0, 1, 1, 0, 0]:

            # Step9: Find distance between fingers
            length, img, lineInfo = detector.findDistance(8, 12, img)

            # Step10: Click mouse if distance short
            if length < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                x3 = np.interp(x1, (frameR, wCam-frameR), (0, wScr))
                y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScr))

                # Step6: Smooth Values
                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening

                # Step7: Move Mouse
                autopy.mouse.click()
                pyautogui.leftClick() 
                # time.sleep(1)
                # Step5: Convert the coordinates
                autopy.mouse.move(wScr - clocX, clocY)
                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                plocX, plocY = clocX, clocY
        
        
        if fingers == [1, 1, 0, 0, 0]:
            length, img, lineInfo = detector.findDistance(4, 8, img)
            if length < 40:
                # cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                cv2.circle(img, (x4, y4), 15, (255, 0, 255), cv2.FILLED)
                pyautogui.rightClick()
                time.sleep(1)
        
        
        # if fingers[0] == 1 and fingers[1] == 1 and fingers[4] == 1:
        #     cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        #     cv2.circle(img, (x4, y4), 15, (255, 0, 255), cv2.FILLED)
        #     cv2.circle(img, (x7, y7), 15, (255, 0, 255), cv2.FILLED)
        #     pyautogui.hotkey('win', 'x')
        #     pyautogui.press('u')
        #     pyautogui.press('s')
        #     time.sleep(2)

        if fingers == [0, 0, 0, 0, 0]:
            pyautogui.hotkey('win', 'd')
            time.sleep(2)

        if fingers == [0, 0, 1, 1, 1]:
            cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x6, y6), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x7, y7), 15, (255, 0, 255), cv2.FILLED)
            pyautogui.alert(text='Screenshot taken', title='checkbox', button='OK')
            pyautogui.hotkey('win', 'printscreen')
            time.sleep(2)

    # Step11: Frame rate
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (28, 58), cv2.FONT_HERSHEY_PLAIN, 3, (255, 8, 8), 3)

    # Step12: Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)