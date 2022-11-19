import time
import cv2
import backup as htm
import numpy as np
import autopy
import math



wCam,hCam = 1366,768
frameR=100
smoothening=5


plocX,plocY=0,0
clocX,clocY=0,0

cap=cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime= 0
detector = htm.handDetector(maxHands=1,detectionCon=0.7)

wScr, hScr =autopy.screen.size()

while True:
    success, img= cap.read()
    img=detector.findHands(img)
    lmList=detector.findPosition(img)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow('mouse', img)
    if cv2.waitKey(1) == ord('q'):
        break


    try:
        if len(lmList)!=0:
            x1,y1=lmList[8][1:]
            x2,y2=lmList[12][1:]
            #print(x1,y1,x2,y2)

        fingers=detector.fingersUp()

        print(fingers)

        cv2.rectangle(img, (frameR,frameR),(wCam-frameR,hCam-frameR), (255, 0, 255), 2)




        if fingers[1] == 1 and fingers[2] == 1:

            length = math.hypot(x2 - x1, y2 - y1)

            if length < 40:
                autopy.mouse.click()


        if fingers[1] == 1 and fingers[2] == 0:

            x3=np.interp(x1,(frameR,wCam-frameR),(0,wScr))
            y3=np.interp(y1,(frameR,hCam-frameR),(0,hScr))

            clocX=plocX+(x3-plocX)/smoothening
            clocY=plocY+(y3-plocY)/smoothening


            autopy.mouse.move(wScr-x2,y3)

            print('sssssssssss')
            cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)




    except:
        print('no hand')








