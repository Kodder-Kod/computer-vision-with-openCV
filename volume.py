import cv2
import time
import numpy as np
import backup as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities,IAudioEndpointVolume

def main():

        wCam, hCam =640,480


        cap =cv2.VideoCapture(0)
        cap.set(3,wCam)
        cap.set(4,hCam)
        pTime = 0

        detector = htm.handDetector(detectionCon=0.7)

        devices =AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL,None)

        volume = cast(interface,POINTER(IAudioEndpointVolume))
        #volume.GetMute()
        #volume.GetMasterVolumeLevel()
        volrange=volume.GetVolumeRange()

        minvol=volrange[0]
        maxvol=volrange[1]
        vol=0
        volbar=400
        volbarper=0



        while True:
            success , img =cap.read()
            img=detector.findHands(img)
            list =detector.findPosition(img, draw=False)




            #if list ==0:
                #print ('')
            #else:
             #print(list[4],list[8])
            # print(list[4])


            try:
                if len(list) !=0:

                 x1, y1 = list[4][1], list[4][2]
                 x2, y2 = list[8][1], list[8][2]
                 cx,cy=(x1+x2) //2,(y1+y2) // 2

                 cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
                 cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
                 cv2.line(img, (x1, y1), (x2,y2),(255, 0, 255), 3)
                 cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                length = math.hypot(x2 - x1, y2 - y1)



                #length=math.hypot(x2-x1,y2-y1)

                print(length)

                vol=np.interp(length,[5,130],[minvol,maxvol])
                volbar= np.interp(length, [5, 130], [400, 150])
                volbarper = np.interp(length, [5, 130], [0, 100])
                #print (int(length),vol)

                volume.SetMasterVolumeLevel(vol, None)

                if length <50:
                    cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

                cv2.rectangle(img, (50, 150), (85,400), (0, 255, 0), 3)
                cv2.rectangle(img, (50, int(volbar)), (85,400), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, str(int(volbarper)), (40, 450), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
            except:
                print('{none}')

            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime

            cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

            cv2.imshow('frame', img)
            if cv2.waitKey(1) == ord('q'):
                break


if __name__ == "__main__":
            main()



