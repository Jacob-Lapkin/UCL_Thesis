import cv2
 
# Opens the Video file
def convertVideo(path):
    cap= cv2.VideoCapture(path)
    i=0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        cv2.imwrite('kang'+str(i)+'.jpg',frame)
        i+=1
    
    cap.release()
    cv2.destroyAllWindows()

convert('videos/serve/nadal/nadalserveside.mp4')