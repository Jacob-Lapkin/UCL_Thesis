import cv2
import os, time, uuid
 
# Opens the Video file
def convertVideo(name):
    cap= cv2.VideoCapture('pose/videos/serve/djok/djokserve45.mp4')
    i=0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        path = '/Users/jacoblapkin/Documents/GitHub/UCL-Thesis/pose/Test'
        cv2.imwrite(os.path.join(path, name +str(i)+'.png'),frame)
        i+=1
    
    cap.release()
    cv2.destroyAllWindows()

convertVideo('djokovic')