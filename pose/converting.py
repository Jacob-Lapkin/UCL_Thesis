import cv2
import os, time, uuid

# Opens the Video file
def converter(path, name):
    cap= cv2.VideoCapture(path)
    i=0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        path = '/Users/jacoblapkin/Documents/GitHub/UCL_Thesis/pose/Test'
        cv2.imwrite(os.path.join(path, name +str(i)+'.jpg'),frame)
        #cv2.imwrite(name+str(i)+'.jpg',frame)
        i+=1
    
    cap.release()
    cv2.destroyAllWindows()

converter('pose/videos/serve/djok/djokserve45.mp4', 'djok')