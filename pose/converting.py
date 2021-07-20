import cv2
import os, time, uuid

# Opens the Video file
def converter(path, name, user):
    cap= cv2.VideoCapture(path)
    i=1
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        path = f'/Users/jacoblapkin/Documents/GitHub/UCL_Thesis/pose/User_test/{user}'
        cv2.imwrite(os.path.join(path, name +str(i)+'.jpg'),frame)
        #cv2.imwrite(name+str(i)+'.jpg',frame)
        i+=1
    
    cap.release()
    cv2.destroyAllWindows()

#converter('pose/videos/serve/djok/djokserveside.mp4', 'djok')

# Creating a directory with the name of id to store frame images
def make_dir(id):
    path = '/Users/jacoblapkin/Documents/GitHub/UCL_Thesis/pose/User_test'
    dir = os.path.join(path, str(id))
    if not os.path.exists(dir):
        os.mkdir(dir)

#make_dir(10)