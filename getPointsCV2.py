import numpy as np
import cv2

def getPointsImage(imagePath):
    width = 700
    height = 700
    image = cv2.imread(imagePath , -1)
    image = cv2.resize(image,(width,height))
    cv2.imshow('Image' , image)
    cv2. waitKey(0)
    cv2.destroyAllWindows()

    

