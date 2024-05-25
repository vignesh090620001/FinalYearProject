import cv2
import numpy as np
def process(path,fname):
        
    image = cv2.imread(path)
      
          
    # Gaussian Blur
    Gaussian = cv2.GaussianBlur(image, (7, 7), 0)
    cv2.imshow('Gaussian Blurring', Gaussian)
    cv2.imwrite("static/Gaussian/"+fname+".jpg",Gaussian)
    cv2.waitKey(0)
      
    # Median Blur
    median = cv2.medianBlur(image, 5)
    cv2.imshow('Median Blurring', median)
    cv2.imwrite("static/Median/"+fname+".jpg",median)
    cv2.waitKey(0)
      
      
    # Bilateral Blur
    bilateral = cv2.bilateralFilter(image, 9, 75, 75)
    cv2.imshow('Bilateral Blurring', bilateral)
    cv2.imwrite("static/Bilateral/"+fname+".jpg",bilateral)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
