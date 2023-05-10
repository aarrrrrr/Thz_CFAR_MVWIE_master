### **Introduction:**

**太赫兹成像技术** 太赫兹波可以透过可见光和红外线所无法穿透的物质或材料，如塑料、陶瓷、绝热泡沫等，所以利用不同的太赫兹成像方式可以与可见光和X射线等成像技术互补。基于太赫兹的高透性和安全性，太赫兹波可透过包装材料进行安检成像。另外，太赫兹成像高分辨率、大景深、安全和无接触性等优点使其在材料研究、安检、医学成像、和军事成像等领域具有广泛的应用前景。目前，成都天府国际机场已经普遍安装了太赫兹安检仪，这项技术逐渐开始进入民众日常的生活领域。

![img](https://pic2.zhimg.com/80/v2-6e00201c1525bd0eb9c11088356a0c15_720w.webp)

为提升安检时违禁物品的识别速度和准确度，神经网络的引入，使得在大部分情况下，无需人工的检测识别，仅凭机器就可以对目标进行识别。本文使用CNN来实现太赫兹安检图像的物体分类。



### **environment:**

pip install tensorflow

pip install numpy

pip install skimage

Python3+



### **explain:**

**datasets：**训练的数据集。受限于太赫兹图像样本数据量太少，笔者从已有的太赫兹图像中截取了“gun”、“phone”、和“people”三种图像目标，并对其进行旋转、平移等变换操作，用来扩充数据集训练和识别。



**binary.py：**读取一张目标图像，二值化处理。



**gene.py：**生成数据增强迭工厂，进行随机旋转、放大缩小、水平垂直翻转等操作，生成扩充的目标图像数据集。



**photos、test：**“gun”、“phone”、和“people”三类目标的数据集和测试集。



**CNN.py：**网络结构及训练。

· 按顺序读入数据集data，每张图片对应的label（上级文件夹名称次序）可以表示所属类别，同时调整输入的数据集图像大小。

· 方便训练，打乱data和label顺序，设置训练集和验证集比例，划分train和val

· 构建网络

​	输入：100*100的图像

​	（1）卷积层，4维tensor，[width, height, channels, kernel_nums]=[5,5,1,32]，32个卷积核，通道数1，卷积核大小为5×5，步长为1，激活函数为 ReLU

​	（2）池化层，窗口大小为2，步长为2

​	（3）卷积层，4维tensor，[width, height, channels, kernel_nums]=[5,5,32,64]，64个卷积核，通道数32，卷积核大小为5×5，步长为1，激活函数为 ReLU

​	（4）池化层，窗口大小为2，步长为2

​	（5）卷积层，4维tensor，[width, height, channels, kernel_nums]=[3,3,64,128]，128个卷积核，通道数64，卷积核大小为3×3，步长为1，激活函数为 ReLU

​	（6）池化层，窗口大小为2，步长为2

​	（7）卷积层，4维tensor，[width, height, channels, kernel_nums]=[3,3,128,128]，128个卷积核，通道数128，卷积核大小为3×3，步长为1，激活函数为 ReLU

​	（8）池化层，窗口大小为2，步长为2

​	（9）全连接层，1024个神经元节点，dropout=0.5

​	（10）全连接层，512个神经元节点，dropout=0.5

​	（11）全连接层，10个神经元节点，输出

· 部分训练结果：

train loss: 0.001370
train acc: 1.000000
validation loss: 0.003785
validation acc: 1.000000



**CNN_test.py：**用于预测验证。

./datasets/test/gun_0_313.jpg识别结果:gun
./datasets/test/gun_0_359.jpg识别结果:gun
./datasets/test/gun_0_713.jpg识别结果:gun
./datasets/test/people_0_715.jpg识别结果:people
./datasets/test/people_0_807.jpg识别结果:people
./datasets/test/people_0_879.jpg识别结果:people
./datasets/test/phone_0.jpg识别结果:phone
./datasets/test/phone_0_3.jpg识别结果:phone
./datasets/test/phone_0_72.jpg识别结果:phone
./datasets/test/phone_0_81.jpg识别结果:phone



**thz_img：**太赫兹安检图像目标检测识别

· 原图像

![thz2](.\thz_img\thz2.bmp)

· 二值化成像。根据太赫兹成像的前后背景灰度特征，区分目标与背景，并阈值分割得到二值化成像。主函数中包含了笔者自己写的OTSU算法和利用cv2.THRESH_OTSU函数来快速成像的部分。

![out1](.\thz_img\out1.jpg)

· 框选目标与识别。二值化后便于探测物体轮廓，再寻找轮廓质心，可以确定物体的矩形框图，以送入网络进行识别，同时在图像上绘制矩形方框和输出CNN识别结果。

![out2](.\thz_img\out2.jpg)



### conclusion：

· 经过训练，CNN在验证集和测试集中的准确率很高，且识别速度较快。

· 应用在太赫兹图像时，根据轮廓判断物体形态和位置的方法速度较快，但是由于OTSU阈值分割的成像图中人体轮廓形成的闭合空隙，会造成轮廓的误识别。这一点可以根据原始的光学图像重叠空隙来相消，或者再构建物体检测网络。









