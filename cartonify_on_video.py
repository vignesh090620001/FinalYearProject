import numpy as np
import cv2
from cartoonize import caart

def process(path,fname):

    videoCaptureObject = cv2.VideoCapture(path)
    frame_width = int(videoCaptureObject.get(3))
    frame_height = int(videoCaptureObject.get(4))
 
    # Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
    out = cv2.VideoWriter('static/video/'+fname+'.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))

    #out = cv2.VideoWriter('videoout.mp4', cv2.VideoWriter_fourcc(*'MP4V'), 24, (720, 1280))
    result = True
    while(result):
        ret,img = videoCaptureObject.read()
        cv2.imshow("original",np.array(img))
        img=caart(img)
        cv2.imshow("cartoon",np.array(img))
        out.write(img)
        if(cv2.waitKey(1) & 0xFF==ord('q')):
            break
    videoCaptureObject.release()
    cv2.destroyAllWindows()
