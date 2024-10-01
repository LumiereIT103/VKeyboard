import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import numpy as np
import cvzone
from pynput.keyboard import Controller

# Initialize camera and set dimensions
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Width
cap.set(4, 720)  # Height
# Initialize hand detector with a detection confidence of 0.8
detector = HandDetector(detectionCon=int(0.8))  # Pass as float

keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]
finalText = ""
keyboard = Controller()

def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        # Draw a filled rectangle (100, 100) to (200, 200) in purple
        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 0, 0), cv2.FILLED)

        # Put text "Q" on the rectangle
        cv2.putText(img, button.text, (x + 25, y + 65),
                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return img

# def drawAll(img, buttonList):
#     imgNew = np.zeros_like(img, np.uint8)
#     for button in buttonList:
#         x, y = button.pos
#         cvzone.cornerRect(imgNew, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
#                           20, rt=0)
#         cv2.rectangle(imgNew, button.pos, (x + button.size[0], y + button.size[1]),
#                       (0, 0, 255 ), cv2.FILLED)
#         cv2.putText(imgNew, button.text, (x + 40, y + 60),
#                     cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
#
#     out = img.copy()
#     alpha = 0
#     mask = imgNew.astype(bool)
#     out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]
#
#     return out  # Move return statement here, after all buttons are processed



class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text


buttonList = []

for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

while True:
    # Capture frame from the webcam
    success, img = cap.read()
    # Find hands and draw landmarks on the image
    img = detector.findHands(img)
    # Get list of hand landmarks and bounding box info
    lmList, bboxinfo = detector.findPosition(img)
    img = drawAll(img, buttonList)

    if lmList:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                # Draw a filled rectangle (100, 100) to (200, 200) in purple
                cv2.rectangle(img, button.pos, (x + w, y + h), (128, 128, 128), cv2.FILLED)

                # Put text "Q" on the rectangle
                cv2.putText(img, button.text, (x + 25, y + 65),
                            cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                l, _, _ = detector.findDistance(8, 12, img, draw=False)
                print(l)

                if l < 30:
                    keyboard.press(button.text)
                    # Draw a filled rectangle (100, 100) to (200, 200) in purple
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)

                    # Put text "Q" on the rectangle
                    cv2.putText(img, button.text, (x + 25, y + 65),
                                cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    finalText += button.text
                    sleep(0.3)

    # Think before when it clicked
    cv2.rectangle(img, (50, 350), (700, 450), (128, 128, 128), cv2.FILLED)
    cv2.putText(img, finalText, (60, 430),
                cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    # Display the image
    cv2.imshow("Image", img)
    # Wait for 1 millisecond between frames
    cv2.waitKey(1)