import numpy as np
import cv2
from cartoonize import caart
def process(path,fname):
    img = cv2.imread(path)
    cv2.imshow("original",np.array(img))
    img=caart(img)
    cv2.imshow("Cartoon",np.array(img))
    cv2.imwrite("static/output/"+fname+".jpg",img)
    cv2.waitKey(0)
#process("./original2.jpg")
    
