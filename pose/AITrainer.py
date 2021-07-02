import cv2
import numpy as np
import time
import PoseModule as pm


def ShotAngle(path, stroke, showall):
    cap = cv2.VideoCapture(path)
    detector = pm.poseDetector()
    while True:
        success, img = cap.read()
        # showall: False shows just points in function while True shows all points on body
        img = detector.findPose(img, showall)
        lmList = detector.findPosition(img, False)
        # print(lmList)
        if len(lmList) != 0:

            # hip2ankle
            angle_right_leg = detector.findAngle(img, 24, 26, 28)
            angle_left_leg = detector.findAngle(img, 23, 25, 27)
            # wrist2shoulder 
            angle_right_arm = detector.findAngle(img, 12, 14, 16)
            angle_left_arm = detector.findAngle(img, 11, 13, 15)
            # shoulder2knee
            angle_right_body = detector.findAngle(img, 12, 24, 26)
            angle_left_body = detector.findAngle(img, 11, 23, 25)
            # elbow2hip
            angle_right_armpit = detector.findAngle(img, 13, 11, 23)
            angle_left_armpit = detector.findAngle(img, 14, 12, 24)

        # Power Level NEED TO FIGURE OUT HOW TO ITERATE OVER FRAMES TO GET AVERAGE, MIN, MAX OF ANGLES
            # leg_power = 0
            # armpit_power = 0
            # arm_power = 0
            # if stroke == 'serve':
            #     if angle_left_leg < 160 and angle_right_leg < 165:
            #         leg_power += 1
            #     if angle_left_armpit > 170 or angle_right_armpit > 170:
            #         arm_power += 1
            #     if angle_left_arm > 170 or angle_right_arm > 170:
            #         armpit_power += 1
            # Power = leg_power  + arm_power + armpit_power


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
                          
        print(angle_left_body)
        cv2.imshow("Image", img)
        cv2.waitKey(1)

ShotAngle('serve/nadal.mov', 'serve', False)

