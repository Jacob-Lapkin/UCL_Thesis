import cv2
import numpy as np
import time
import PoseModule as pm



def ShotAngle(path, stroke, angle_type):
    cap = cv2.VideoCapture(path)
    detector = pm.poseDetector()
    angleList = []
    while True:
        success, img = cap.read()

        bad_frame = True
        if success:
            pass
        else:
            bad_frame = False
        # showall: False shows just points in function while True shows all points on body
        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)
        # print(lmList)
        if len(lmList) != 0:
            if angle_type == 0:
                # hip2ankle
                angle_right_leg = detector.findAngle(img, 24, 26, 28)
                angle_left_leg = detector.findAngle(img, 23, 25, 27)
            
            elif angle_type == 1:
                # wrist2shoulder 
                angle_right_arm = detector.findAngle(img, 12, 14, 16)
                angle_left_arm = detector.findAngle(img, 11, 13, 15)

            elif angle_type == 2:
                # shoulder2knee
                angle_right_body = detector.findAngle(img, 12, 24, 26)
                angle_left_body = detector.findAngle(img, 11, 23, 25)
            
            elif angle_type == 3:
                # elbow2hip
                angle_right_armpit = detector.findAngle(img, 13, 11, 23)
                angle_left_armpit = detector.findAngle(img, 14, 12, 24)

            elif angle_type == 4:
                # all angles
                angle_right_leg = detector.findAngle(img, 24, 26, 28)
                angle_left_leg = detector.findAngle(img, 23, 25, 27)
                angle_right_arm = detector.findAngle(img, 12, 14, 16)
                angle_left_arm = detector.findAngle(img, 11, 13, 15)
                angle_right_body = detector.findAngle(img, 12, 24, 26)
                angle_left_body = detector.findAngle(img, 11, 23, 25)
                angle_right_armpit = detector.findAngle(img, 13, 11, 23)
                angle_left_armpit = detector.findAngle(img, 14, 12, 24)
                

            # Draw  Count
            # X cordinate 
            shape = img.shape
            xShape = shape[1]
            alignX = xShape * 0.7

            # Y cordinate 
            yshape = img.shape
            yShape = yshape[0]
            alignY = yShape * 0.05
            
            cv2.putText(img, 'Test', (int(alignX), int(alignY)), cv2.FONT_HERSHEY_PLAIN, 2,
                        (0, 255, 255), 2)  
              
            if cv2.waitKey(10) & 0xFF == ord('q') or bad_frame == False:
                #return empty
                break
        
        #print(angle_right_leg)          
        cv2.imshow("Image", img)
        cv2.waitKey(1)
    
ShotAngle('pose/videos/serve/nadal/nadalserveside.mp4', 'serve', 4)

