import numpy as np
import cv2
from operator import itemgetter

def getPointsImage(imagePath):
    #Set width and height of the image
    width = 700
    height = 700
    #Set border
    x_border = 20
    y_border = 20
    #Escalar transformacion
    escalar = 100
    #Load image from imagePath
    image = cv2.imread(imagePath , -1)
    #Check if imagePath is correct
    if image is None:
        return False, 0, 0
    #Create HSV image and save in files
    image = cv2.resize(image,(width,height))
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    cv2.imwrite('assets/imgMod/hsv.jpeg',hsv)
    #Create image with recognized  points
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
    #Image data recolection
    #Use the average value from each point
    #Create empty list
    points= []
    for j in range (x_border,width-x_border):
        x_point= []
        for i in range (y_border, height-y_border):
            if(mask[i,j]==255):
                x_point.append((j,i))
        if(len(x_point)>0):
            x_array = np.mean(x_point,axis=0 ,dtype=np.int32)
            points.append((x_array[0],x_array[1]))
    if len(points) == 0:
        return False, 0, 0
    #Now the list points has the values of the graph
    points_array = np.array(points)
    #Create image
    img_points = image
    #Get the greater and the lower points in Y
    min_value = points_array[np.argmin(points_array[:,1])]
    max_value = points_array[np.argmax(points_array[:,1])]
    #Draw the greater and lower points
    img_points = cv2.circle(img_points, min_value, 20, (255,0,255), -1)
    img_points = cv2.circle(img_points, max_value, 20, (255,0,255), -1)
    list_points = []
    for point in (points_array[::5]):
        img_points = cv2.circle(img_points, point, 8, (0,0,255), -1)
        list_points.append((point[0],point[1]))
    
    #Write text points
    font = cv2.FONT_HERSHEY_SIMPLEX
    img_points = cv2.putText(img_points, 'P1',(min_value[0]-50,min_value[1]),font,1.5, (0,0,0), 3, cv2.LINE_AA)
    img_points = cv2.putText(img_points, 'P2',(max_value[0],max_value[1]+50),font,1.5, (0,0,0), 3, cv2.LINE_AA)
    #Save the image with points in files
    cv2.imwrite('assets/imgMod/points.jpeg',img_points)
    #Add min and max to the list_points
    list_points.append((min_value[0],min_value[1]))
    list_points.append((max_value[0],max_value[1]))
    #Remove repeated elements
    list_points = list(dict.fromkeys(list_points))
    #Sort list
    list_points.sort(key=itemgetter(0))
    #Create numpy array
    points_array = np.array(list_points)
    #Transform to x,y form and divide by 100
    points_array[:,1] =  (points_array[:,1] *-1)+height
    points_array = points_array / escalar
    #Transform to list form
    list_points = points_array.tolist()
    maxPoint = (max_value[0]/escalar,((max_value[1]*-1)+height)/escalar)
    minPoint = (min_value[0]/escalar,((min_value[1]*-1)+height)/escalar)
    #Return list, minpoint, maxpoint
    return list_points, maxPoint, minPoint

def transformPoints(points, smaller, bigger, rSmaller, rBigger):
    #Linear transformation using this 2 points as ref
    #X1,Y1
    x1 = smaller[0]
    y1 = smaller[1]
    #Xt1, Yt1
    xt1 = rSmaller[0]
    yt1 = rSmaller[1]

    #X2,Y2
    x2 = bigger[0]
    y2 = bigger[1]
    #Xt2, Yt2
    xt2 = rBigger[0]
    yt2 = rBigger[1]
    #Find min and max point
    minX = min(xt1,xt2)
    maxX = max(xt1,xt2)
    minY = min(yt1,yt2)
    maxY = max(yt1,yt2)
    #Calc difX and difY
    difX = (maxX-minX)/(abs(x2-x1))
    difY = (maxY-minY)/(abs(y2-y1))
    #Calc minX2 minY2
    minX2 = min(x1,x2)
    minY2 = min(y1,y2)
    #Create numpy array
    points_array = np.array(points)
    point_transform = []
    point_transform.append((xt1,yt1))
    point_transform.append((xt2,yt2))
    #Transform elements
    for point in points_array:
        x = point[0]
        y = point[1]
        Lx = minX + (difX)*(x-minX2)
        Ly = minY + (difY)*(y-minY2)
        point_transform.append((Lx,Ly))
    point_transform.sort(key=itemgetter(0))
    point_transform = list(dict.fromkeys(point_transform))
    return point_transform


