import cv2
import numpy as np
import time
import PoseModule as pm


def ShotAngle(path, p1, p2, p3, p4, p5, p6, showall):
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
            angle_right = detector.findAngle(img, p1, p2, p3)
            angle_left = detector.findAngle(img, p4, p5, p6)
            
            #angle = detector.findAngle(img, 11, 13, 15,False)
            per = np.interp(angle_right, (210, 310), (0, 100))
            bar = np.interp(angle_right, (220, 310), (650, 100))
            # print(angle, per)

            # Check for the tennis attribute
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

            #  Draw Bar
            # cv2.rectangle(img, (400, 100), (400, 1000), color, 3)
            # cv2.rectangle(img, (400, int(bar)), (400, 1000), color, cv2.FILLED)
            # cv2.putText(img, str(int(per)), (400, 75), cv2.FONT_HERSHEY_PLAIN, 4,
            #             color, 4)

            # # Draw  Count
            # # X cordinate 
            # shape = img.shape
            # xShape = shape[1]
            # alignX = xShape * 0.85
            # x_int_align = int(alignX)

            # # Y cordinate 
            # yshape = img.shape
            # yShape = yshape[0]
            # alignY = yShape * 0.1
            # y_int_align = int(alignY)
            
            # cv2.putText(img, str(int(count)), (x_int_align, y_int_align), cv2.FONT_HERSHEY_PLAIN, 8,
            #             (255, 0, 0), 10)      

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
                    (255, 0, 0), 5)

        cv2.imshow("Image", img)
        cv2.waitKey(1)

ShotAngle(path = 'Kach.mp4', p1 = 24, p2 = 26, p3 = 28, p4=23, p5=25, p6=27, showall=False)