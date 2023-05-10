import cv2
import numpy as np
 
img = cv2.imread("thz1.jpg")   #读取图片
#img = cv2.resize(img,(1000,600))
w,h = img.shape[:-1]  #获取长宽
# print(w,h)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  #变为灰度图 
ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)##阈值分割得到二值化图片
# cv2.namedWindow('binary', cv2.WINDOW_AUTOSIZE)
# cv2.imshow('binary', binary)
# cv2.waitKey(0)
 
contours,heriachy = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
for i ,contour in enumerate(contours):
    # print(contour[:,0])
    a = sorted(contour[:,0], key=lambda x:x[0])  #所有坐标按x轴从小到大排序
    x_min = a[0][0]
    x_max = a[-1][0]
    b = sorted(contour[:,0], key=lambda x:x[1])  #所有坐标按y轴从小到大排序
    y_min = b[0][1]
    y_max = b[-1][1]
    cv2.drawContours(img,contours,i,(0,0,255),1)
    #第一个参数指在哪幅图上绘制轮廓信息，第二个参数是轮廓本身，第三个参数是指定绘制哪条轮廓
    #第四个参数是绘图的颜色，第五个参数是绘制的线宽 输入-1则表示填充
    cv2.rectangle(img,(x_min,y_min),(x_max,y_max),(0,255,0),2)
    print(i)
    
cv2.imshow("detect contours",img)
cv2.waitKey(0)