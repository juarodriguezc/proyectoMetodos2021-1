import numpy as np
import cv2
import matplotlib.pyplot as plt
import VectorToPolinomio as VTP

#Load image from assets
img = cv2.imread('assets/img_test_detection3.jpeg' , -1)
    #-1, IMREAD_COLOR: Color image mode No transparent
    #0, IMREAD_FRAYSCALE: Grayscale mode
    #1, IMREAD_UNCHANGED: Color image Transparent background
#Seet width and height
width = 700
height = 700
#Create border 
x_border = 20
y_border = 20
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
#Remove border results
mask[0:height,0:x_border] = 0
mask[0:height,width-x_border:width] = 0
mask[0:y_border,0:width] = 0
mask[height-y_border:height,0:width] = 0
#Create window with image
cv2.imshow('Image' , mask)
cv2. waitKey(0)
cv2.destroyAllWindows()
#Image data recolection
#Use the average value from each point
#Create empty np.array
points= []
for j in range (x_border,width-x_border):
    x_point= []
    for i in range (y_border, height-y_border):
        if(mask[i,j]==255):
            x_point.append((j,i))
    if(len(x_point)>0):
        x_array = np.mean(x_point,axis=0 ,dtype=np.int32)
        points.append((x_array[0],x_array[1]))
#Now the list points has the values of the graph
points_array = np.array(points)
list_points = []
img_points = img
for point in (points_array[::30]):
    img_points = cv2.circle(img_points, point, 5, (0,0,255), -1)
    list_points.append(point)
cv2.imshow('Image' , img_points)
cv2. waitKey(0)
cv2.destroyAllWindows()


plt.imshow(mask)
plt.show()

plt.plot((points_array[::30,1]),'o')
plt.show()