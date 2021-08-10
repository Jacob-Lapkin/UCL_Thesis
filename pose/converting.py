import cv2
import os, time, uuid, shutil


def delete_user_video(user):
    folder = f'/Users/jacoblapkin/Documents/GitHub/UCL_Thesis/pose/user_serves/{user}'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def delete_frames(user):
    folder = f'/Users/jacoblapkin/Documents/GitHub/UCL_Thesis/pose/User_test/{user}'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def is_empty(user):
    path = f'/Users/jacoblapkin/Documents/GitHub/UCL_Thesis/pose/user_serves/{user}'
    if len(os.listdir(path)) == 0:
        return True
    else:    
        False

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

#converter('pose/videos/serve/djok/djokserveside.mp4', 'djok', '1')

# Creating a directory with the name of id to store frame images
def make_frame_dir(id):
    path = '/Users/jacoblapkin/Documents/GitHub/UCL_Thesis/pose/User_test'
    dir = os.path.join(path, str(id))
    if not os.path.exists(dir):
        os.mkdir(dir)

def make_video_dir(id):
    path = '/Users/jacoblapkin/Documents/GitHub/UCL_Thesis/pose/user_serves'
    dir = os.path.join(path, str(id))
    if not os.path.exists(dir):
        os.mkdir(dir)

# def is_empty(id):
#     path = '/Users/jacoblapkin/Documents/GitHub/UCL_Thesis/pose/user_serves'
#     dir = os.path.join(path, str(id))
#     if not os.path.exists(dir):

#make_dir(10)






