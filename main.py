import numpy as np
import cv2
import matplotlib.pyplot as plt
import VectorToPolinomio as VTP

from operator import itemgetter

#Load image from assets
#img = cv2.imread('assets/test_graph.JPG' , -1)
img = cv2.imread('assets/img_test_detection2.jpeg' , -1)
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
for point in (points_array[::]):
    img_points = cv2.circle(img_points, point, 8, (0,0,255), -1)
    list_points.append(point)



cv2.imshow('Image' , img_points)
cv2. waitKey(0)
cv2.destroyAllWindows()

#Transform to graph form
points_array[:,1] =  (points_array[:,1] *-1)+height


min_value = points_array[np.argmin(points_array[:,1])]
max_value = points_array[np.argmax(points_array[:,1])]




#Linear transformation using this 2 points as ref

#X1,Y1
x1 = min_value[0]
y1 = min_value[1]

#Xt1, Yt1
xt1 = -1
yt1 = 5

#X2,Y2
x2 = max_value[0]
y2 = max_value[1]

#Xt2, Yt2
xt2 = 1
yt2 = 7

minX = min(xt1,xt2)
maxX = max(xt1,xt2)
minY = min(yt1,yt2)
maxY = max(yt1,yt2)

print("minX: ",minX, " minY: ",minY)
print("maxX: ",maxX, " maxY: ",maxY)

difX = (maxX-minX)/(abs(x2-x1))
difY = (maxY-minY)/(abs(y2-y1))


minX2 = min(x1,x2)
minY2 = min(y1,y2)



print(difX)
print(difY)


points_array =  (points_array[20:680:40])
point_transform = []
point_transform.append((xt1,yt1))
point_transform.append((xt2,yt2))



for point in points_array:
    x = point[0]
    y = point[1]
    #Calc linear transformation
    #calc x
    #Lx = xt1*((x*y2-x2*y)/(x1*y2-x2*y1)) + xt2*((x1*y-x*y1)/(x1*y2-x2*y1))
    #Calc y
    #Ly = yt1*((x*y2-x2*y)/(x1*y2-x2*y1)) + yt2*((x1*y-x*y1)/(x1*y2-x2*y1))


    Lx = minX + (difX)*(x-minX2)
    Ly = minY + (difY)*(y-minY2)

    print("Lx: ",Lx,"  Ly: ",Ly)
    point_transform.append((Lx,Ly))




point_transform2 = point_transform.sort(key=itemgetter(0))

x_val = [x[0] for x in point_transform]
y_val = [x[1] for x in point_transform]

plt.plot(x_val,y_val,'o')
plt.show()

x_val = [x[0] for x in points_array]
y_val = [x[1] for x in points_array]

plt.plot(x_val,y_val,'o')
plt.show()

