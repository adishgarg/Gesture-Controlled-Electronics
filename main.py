from cvzone.HandTrackingModule import HandDetector
import cv2
import time
from cvzone.SerialModule import SerialObject

arduino = SerialObject("COM5")

cap = cv2.VideoCapture(1)


detector = HandDetector(staticMode=False,
                        maxHands=2,
                        modelComplexity=1,
                        detectionCon=0.6,
                        minTrackCon=0.7)

while True:

    success, img = cap.read()

    hands, img = detector.findHands(img, draw=True, flipType=True)


    if hands:
        hand1 = hands[0]
        lmList1 = hand1["lmList"]
        bbox1 = hand1["bbox"]
        center1 = hand1['center']
        handType1 = hand1["type"]


        fingers1 = detector.fingersUp(hand1)
        print(f'H1 = {fingers1.count(1)}', end=" ")

        tipOfIndexFinger = lmList1[8][0:2]
        tipOfThumb = lmList1[4][0:2]
        tipOfMiddleFinger =lmList1[12][0:2]
        length1, info, img = detector.findDistance(tipOfIndexFinger,tipOfThumb , img, color=(255, 0, 255),
                                                  scale=5)
        length2, info, img = detector.findDistance(tipOfMiddleFinger, tipOfThumb, img, color=(255, 0, 255),
                                                   scale=5)
        print(length1)

        if len(hands) == 2:
            hand2 = hands[1]
            lmList2 = hand2["lmList"]
            bbox2 = hand2["bbox"]
            center2 = hand2['center']
            handType2 = hand2["type"]

            fingers2 = detector.fingersUp(hand2)
            print(f'H2 = {fingers2.count(1)}', end=" ")
            tipOfIndexFinger2 = lmList2[8][0:2]
            tipOfThumb2=lmList2[4][0:2]
            length, info, img = detector.findDistance(tipOfThumb2,tipOfIndexFinger2 , img, color=(255, 0, 255),
                                                  scale=5)
            print(length)
        if len(hands)==1:
            if fingers1.count(1) == 1:
                arduino.sendData([0])
                # arduino.sendData([225])
            elif fingers1.count(1) == 2:
                arduino.sendData([1])
                # arduino.sendData([225])
            elif fingers1.count(1) == 3:
                arduino.sendData([2])
                # arduino.sendData([225])
            elif fingers1.count(1)==4:
                arduino.sendData([3])
                # arduino.sendData([225])
            elif fingers1.count(1)==5:
                arduino.sendData([4])
                # arduino.sendData([225])
        elif len(hands)==2:
            if handType1 == "Left":
                if fingers2.count(1) == 1:
                    arduino.sendData([0])
                    arduino.sendData(([int(length1)* 20]))
                elif fingers2.count(1) == 2:
                    arduino.sendData([1])
                    arduino.sendData([int(length1) * 20])
                elif fingers2.count(1) == 3:
                    arduino.sendData([2])
                    arduino.sendData([int(length1) * 20])
                elif fingers2.count(1) == 4:
                    arduino.sendData([3])
                    arduino.sendData([int(length1) * 20])
                elif fingers2.count(1) == 5:
                    arduino.sendData([4])
                    arduino.sendData([int(length1) * 20])
            elif handType1 == "Right":
                if fingers1.count(1) == 1:
                    arduino.sendData([0])
                    arduino.sendData(([int(length2)* 20]))
                elif fingers1.count(1) == 2:
                    arduino.sendData([1])
                    arduino.sendData([int(length2) * 20])
                elif fingers1.count(1) == 3:
                    arduino.sendData([2])
                    arduino.sendData([int(length2) * 20])
                elif fingers1.count(1) == 4:
                    arduino.sendData([3])
                    arduino.sendData([int(length2) * 20])
                elif fingers1.count(1) == 5:
                    arduino.sendData([4])
                    arduino.sendData([int(length2) * 20])


        print(" ")


    cv2.imshow("Image", img)


    cv2.waitKey(1)

