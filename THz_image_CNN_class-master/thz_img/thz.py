import cv2
from PIL import Image
import numpy as np
from skimage import io,transform
from matplotlib import pyplot
from scipy.signal import savgol_filter
import scipy.signal
import recg_func

nam='thz2'
ori=nam+'.bmp'
#%% my成像
# I = Image.open(ori)
# #I.show()
# L = I.convert('L')
# #L.show()
# p0=np.asarray(L)
# p1 = cv2.blur(p0,(3,3))
# rows,cols = p1.shape
# x=p1.reshape(rows*cols)
# y=np.zeros((256))
# for i in range(len(x)):
#     loc=x[i]
#     y[loc]=y[loc]+1
# y_smo = savgol_filter(y, 50, 3, mode= 'nearest')
# # pyplot.plot(y_smo)
# # maxpole=scipy.signal.argrelmax(y_smo) # 极大值 的下标
# minpole=scipy.signal.argrelmin(y_smo) # 极小值 的下标
# minpole=np.array(minpole)
# derta=abs(minpole-128)
# min_index=np.argmin(derta)
# minp=minpole[0,min_index]
# A = np.argmax(y_smo[0:minp])
# B = np.argmax(y_smo[minp:len(y_smo)])+minp
# p2=np.zeros((rows,cols))
# for i in range(rows):
#     for j in range(cols):
#         if p1[i,j]<A:
#             p2[i,j]=0
#         elif p1[i,j]>B:
#             p2[i,j]=255
#         else:
#             p2[i,j]=(p1[i,j]-A)*255/(B-A);        
# p2=np.array(p2,dtype='uint8')
# # p2=Image.fromarray(p2)
# # p2.show()

# p3 = scipy.signal.medfilt(p2, kernel_size=5)
# # p3=Image.fromarray(p3)
# # p3.show()

# p4=p3;
# g=np.zeros((256,1));
# for t in range(1,256):
#     fore=np.zeros((rows*cols,2));
#     back=np.zeros((rows*cols,2));
#     for i in range(rows):
#         for j in range(cols):
#             if(p4[i,j]>=t):
#                 fore[i*cols+j,0]=p4[i,j];
#                 fore[i*cols+j,1]=1;
#             else:
#                 back[i*cols+j,0]=p4[i,j];
#                 back[i*cols+j,1]=1;
#     N=rows*cols;
#     W0=0;
#     U0=0;
#     for ii in range(rows*cols):
#         if(fore[ii,1]==1):
#             W0=W0+1;
#             U0=U0+fore[ii,0];
#     U0=U0/W0;
#     W0=W0/N;
    
#     W1=0;
#     U1=0;
#     for ii in range(rows*cols):
#         if(back[ii,1]==1):
#             W1=W1+1;
#             U1=U1+back[ii,0];
#     U1=U1/W1;
#     W1=W1/N;
    
#     U=W0*U0+W1*U1;
#     g[t]=W0*(U0-U)*(U0-U)+W1*(U1-U)*(U1-U)

# T=np.argmax(g);

# for i in range(rows):
#     for j in range(cols):
#         if(p4[i,j]>=T):
#             p4[i,j]=255;
#         else:
#             p4[i,j]=0;
#%% 成像结果
# p4out=Image.fromarray(p4)
# p4out.save('thz1.jpg')
# p4out.show()
#%% 简易成像
easy = cv2.imread(ori)   #读取图片
#img = cv2.resize(img,(1000,600))
easy = cv2.blur(easy,(3,3))
easy = scipy.signal.medfilt(easy, kernel_size=5)
w,h = easy.shape[:-1]  #获取长宽
# print(w,h)
gray = cv2.cvtColor(easy, cv2.COLOR_BGR2GRAY)  #变为灰度图 
ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)##阈值分割得到二值化图片
cv2.imshow("bin",binary)
cv2.waitKey(0)
p4=binary
#%%原图像
# real = cv2.imread(nam+'_real.bmp')   #读取图片
# real = cv2.blur(real,(3,3))
# real = scipy.signal.medfilt(real, kernel_size=5)
# real = cv2.cvtColor(real, cv2.COLOR_BGR2GRAY)  #变为灰度图 
# ret, binary_real = cv2.threshold(real, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_TRIANGLE)##阈值分割得到二值化图片
# binary_real = scipy.signal.medfilt(binary_real, kernel_size=5)

# contours,heriachy = cv2.findContours(binary_real,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
# cv2.drawContours(real,contours,-1,(255,255,255),1)
# cv2.imshow("bin",binary_real)
# cv2.waitKey(0)
#%% 
p5=p4
img = cv2.imread(ori)
rows,cols = p5.shape#获取长宽

# cv2.namedWindow('binary', cv2.WINDOW_AUTOSIZE)
# cv2.imshow('binary', p5)
# cv2.waitKey(0)
 
contours,heriachy = cv2.findContours(p5,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
for i ,contour in enumerate(contours):
    # print(contour[:,0])
    a = sorted(contour[:,0], key=lambda x:x[0])  #所有坐标按x轴从小到大排序
    x_min = a[0][0]
    x_max = a[-1][0]
    b = sorted(contour[:,0], key=lambda x:x[1])  #所有坐标按y轴从小到大排序
    y_min = b[0][1]
    y_max = b[-1][1]
    l=max(x_max-x_min,y_max-y_min)
    l2=int(l/2)
    y_cen=int((y_min+y_max)/2)
    x_cen=int((x_min+x_max)/2)
    if(y_cen-l2>=0 and y_cen+l2<rows and x_cen-l2>=0 and x_cen+l2<cols):
        pices=p5[y_cen-l2:y_cen+l2,x_cen-l2:x_cen+l2]
    else:
        pices=p5[y_min:y_max,x_min:x_max]
    
    if(np.size(pices,axis=None)>=9):
        out=recg_func.recgfun(pices)
    else:
        # out='nothing'
        continue
    print(out)
    
    cv2.drawContours(img,contours,i,(0,0,255),1)
    #第一个参数指在哪幅图上绘制轮廓信息，第二个参数是轮廓本身，第三个参数是指定绘制哪条轮廓
    #第四个参数是绘图的颜色，第五个参数是绘制的线宽 输入-1则表示填充
    cv2.rectangle(img,(x_min,y_min),(x_max,y_max),(0,255,0),1,)
    cv2.putText(img, out,
                (x_min,y_min),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 0, 0),
                thickness=1
                )
    print(i)
    
cv2.imshow("detect contours",img)
cv2.waitKey(0)








































