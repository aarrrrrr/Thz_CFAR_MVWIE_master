# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 11:42:13 2022

@author: 21114
"""
import cv2
import numpy as np
 
img = cv2.imread("phone_0_0.jpg")   #读取图片
#img = cv2.resize(img,(1000,600))
w,h = img.shape[:-1]  #获取长宽
print(w,h)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  #变为灰度图 
ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)##阈值分割得到二值化图片
cv2.imwrite("phone_0.jpg",binary)
