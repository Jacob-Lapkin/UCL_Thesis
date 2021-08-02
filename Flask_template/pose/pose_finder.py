import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle 




def angle_from_video(path):
    empty_left_leg = []
    empty_right_leg = []
    empty_right_arm = []
    empty_left_arm = []
    empty_right_body = []
    empty_left_body = []


    frame_count = []
    cap = cv2.VideoCapture(path)
    #cap = cv2.VideoCapture(0)
    ## Setup mediapipe instance
    
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
            frame_count.append(current_frame)
            #number_of_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            #Recolor image to RGB
            bad_frame = True
            if ret:
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                bad_frame = False
            image.flags.writeable = False
        
            # Make detection
            results = pose.process(image)
        
            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                
                # Get coordinates
                # for left shoulder to left wrist angle
                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                # for right shoulder to right wrist angle
                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                
                # for left hip to left ankle ankle
                left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                # for right hip to right ankle angle
                right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

                # for left elbow to left hip
                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                # for right elbow to right hip
                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]


                # Calculate angle leg 
                angle_left_leg = calculate_angle(left_hip, left_knee, left_ankle)
                angle_right_leg = calculate_angle(right_hip, right_knee, right_ankle)
                empty_left_leg.append(angle_left_leg)
                empty_right_leg.append(angle_right_leg)
                

                # Calculate angle arm
                angle_left_arm = calculate_angle(left_shoulder, left_elbow, left_wrist)
                angle_right_arm = calculate_angle(right_shoulder, right_elbow, right_wrist)
                empty_left_arm.append(angle_left_arm)
                empty_right_arm.append(angle_right_arm)

                # Calculate angle body
                angle_left_body = calculate_angle(left_elbow, left_shoulder, left_hip)
                angle_right_body = calculate_angle(right_elbow, right_shoulder, right_hip)
                empty_left_body.append(angle_left_body)
                empty_right_body.append(angle_right_body)

                print(angle_right_body, angle_left_body)
                print(current_frame)

                # Visualize angle
                cv2.putText(image, str(angle_right_arm), 
                            tuple(np.multiply(left_elbow, [640, 480]).astype(int)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

                cv2.putText(image, str(angle_left_arm), 
                            tuple(np.multiply(right_elbow, [640, 480]).astype(int)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                    )
                        
            except:
                pass
            

            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                    )                   

            cv2.imshow('Mediapipe Feed', image)
            if cv2.waitKey(10) & 0xFF == ord('q') or bad_frame == False:
                d = {'frame':frame_count,'hip2ankle_left':empty_left_leg, 'hip2ankle_right':empty_right_leg,
                 'shoulder2wrist_left':empty_left_arm, 'shoulder2wrist_right':empty_right_arm, 'elbow2hip_left': empty_left_body, 'elbow2hip_right': empty_right_body}
                df = pd.DataFrame(d)
                return df
                break 
        
        cap.release()
        cv2.destroyAllWindows()


print(angle_from_video('Flask_template/pose/videos/serve/djok/djokserveside.mp4'))

def user_data(path):
    df = angle_from_video(path)
    writer = pd.ExcelWriter('output.xlsx')
    export = df.to_excel(writer)
    writer.save()
    return export

#print(user_data('pose/videos/serve/djok/djokserveside.mp4'))