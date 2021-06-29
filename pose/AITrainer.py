import cv2
import numpy as np
import time
import PoseModule as pm


def ShotAngle(path, p1, p2, p3, showall):
    cap = cv2.VideoCapture(path)
    detector = pm.poseDetector()
    count = 0
    dir = 0
    pTime = 0
    while True:
        success, img = cap.read()
        
        # showall: False shows just points in function while True shows all points on body
        img = detector.findPose(img, showall)
        lmList = detector.findPosition(img, False)
        # print(lmList)
        if len(lmList) != 0:

            # Angle Function
            angle = detector.findAngle(img, p1, p2, p3)
            
            #angle = detector.findAngle(img, 11, 13, 15,False)
            per = np.interp(angle, (210, 310), (0, 100))
            bar = np.interp(angle, (220, 310), (650, 100))
            # print(angle, per)

            # Check for the dumbbell curls
            color = (255, 0, 255)
            if per == 100:
                color = (0, 255, 0)
                if dir == 0:
                    count += 0.5
                    dir = 1
            if per == 0:
                color = (0, 255, 0)
                if dir == 1:
                    count += 0.5
                    dir = 0
            print(count)

            # Draw Bar

            cv2.rectangle(img, (400, 100), (400, 1000), color, 3)
            cv2.rectangle(img, (400, int(bar)), (400, 1000), color, cv2.FILLED)
            cv2.putText(img, str(int(per)), (400, 75), cv2.FONT_HERSHEY_PLAIN, 4,
                        color, 4)

            # Draw Curl Count
            # X cordinate 
            shape = img.shape
            xShape = shape[1]
            alignX = xShape * 0.85
            intAlign = int(alignX)

            # Y cordinate 
            yshape = img.shape
            yShape = yshape[0]
            alignY = yShape * 0.1
            YintAlign = int(alignY)

            cv2.putText(img, str(int(count)), (intAlign, YintAlign), cv2.FONT_HERSHEY_PLAIN, 8,
                        (255, 0, 0), 15)      

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
                    (255, 0, 0), 5)

        cv2.imshow("Image", img)
        cv2.waitKey(1)

ShotAngle(path = 'Posp.mp4', p1 = 24, p2 = 26, p3 = 28, showall=False)