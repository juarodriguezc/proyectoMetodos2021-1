import cv2

img = cv2.imread('assets/img_template.jpeg' , 0)
#-1, IMREAD_COLOR: Color image mode No transparent
#0, IMREAD_FRAYSCALE: Grayscale mode
#1, IMREAD_UNCHANGED: Color image Transparent background
img = cv2.resize(img,(700,700))
#img = cv2.rotate(img,cv2.cv2.ROTATE_90_CLOCKWISE)
cv2.imwrite('assets/template_img_resized.jpeg',img)
cv2.imshow('Image' , img)
cv2.waitKey(0)
cv2.destroyAllWindows()


print("Proyecto métodos 2021-1")

