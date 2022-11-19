import cv2
import mediapipe as mp
import time
import math


class handDetector():
    def __init__(self, mode=False, maxHands=2, model=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.model = model

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.model, self.detectionCon,  self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds=[4,8,12,16,20]

    def findHands(self, img, draw=True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(imgRGB)

        if self.result.multi_hand_landmarks:
            for handLms in self.result.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS )
        return img




    def findPosition(self, img,handNo=0, draw=True):

        self.lmList = []
        xList=[]
        yList=[]
        bbox=[]
        if self.result.multi_hand_landmarks:
            myHand = self.result.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):
                #print(id, lm)
                h,w,c= img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                #print (id, cx, cy)

                #list=[cx,cy]
                #lmList={id:list}

                xList.append(cx)
                yList.append(cy)
                self.lmList.append([id,cx,cy])
                #if len(lmList) !=0:
                   #print(lmList[4])
            xmin,xmax=min(xList),max(xList)
            ymin,ymax=min(yList),max(yList)
            bbox=xmin,ymin,xmax,ymax

            if draw:
                    cv2.circle(img,(cx,cy),1,(0,255,0), cv2.FILLED)


            return self.lmList

    def fingersUp(self):
            fingers = []
            # thumb
            if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
                # fingers
                for id in range(1, 5):
                    if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                #totalFingers = fingers.count(1)
                return fingers


    def findDistance(self,p1,p2,img, draw=True,r=15,t=3):
        x1,y1=self.lmList[p1][1:]
        x2,y2=self.lmList[p2][1:]
        cx,cy=(x1+x2)//2,(y1+y2)//2

        if draw:
            cv2.line(img,(x1,y1),(x2,y2),(255,0,255),t)
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2),r, (255, 0, 255), cv2.FILLED)
            cv2.cirle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
        length= math.hypot(x2-x1,y2-y1)

        return length,img [x1,y1,x2,y2,cx,cy]




def main():
    pTime = 0
    cTime = 0

    Wcam, hCam = 720, 640

    cap = cv2.VideoCapture(0)
    cap.set(3, Wcam)
    cap.set(4,hCam)
    detector = handDetector()

    while True:
        success, img = cap.read()
         #ret, frame = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)

        try:
            if len(list) != 0:
                print(list[4])
        except:
            print('[]')

        #for i in lmList:
        #print(lmList)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)



        cv2.imshow("Image", img)
        if cv2.waitKey(1) == ord('q'):
            break


if __name__=="__main__":
    main()



