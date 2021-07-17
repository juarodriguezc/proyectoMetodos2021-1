import numpy as np
import cv2
import random
import matplotlib.pyplot as plt
#Load image from assets
img = cv2.imread('assets/img_test_detection2.jpeg' , -1)
    #-1, IMREAD_COLOR: Color image mode No transparent
    #0, IMREAD_FRAYSCALE: Grayscale mode
    #1, IMREAD_UNCHANGED: Color image Transparent background
#Seet width and height
width = 700
height = 700
#Resize the image
img = cv2.resize(img,(width,height))
#Create a copy of the image with HSV color
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
cv2.imwrite('assets/img_hsv_test.jpeg',hsv)
#Set color range to extract
lower_blue = np.array([110,50,50])
upper_blue = np.array([130,255,255])
#Create mask
mask = cv2.inRange(hsv, lower_blue,upper_blue)
#Create window with image
cv2.imshow('Image' , mask)
cv2. waitKey(0)
cv2.destroyAllWindows()
#Image data recolection
#Use the average value from each point
#Create empty np.array
print(type(mask))
mask[584:598,534:548] = 255
cv2.imshow('Image' , mask)
cv2. waitKey(0)
cv2.destroyAllWindows()
plt.imshow(mask)
plt.show()