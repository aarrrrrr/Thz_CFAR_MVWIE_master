# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 22:22:38 2022

@author: 21114
"""
import tensorflow as tf
# 综合增强示例
from tensorflow import keras
from numpy import expand_dims
from matplotlib import pyplot
# 读入图片
name='phone'
img_path='D:/college/python/myproject/thz_recg/CNN_Image_class-master/datasets/gendata/'+name+'_0.jpg'
img = tf.keras.preprocessing.image.load_img(img_path)
pyplot.imshow(img)
# 转换为 numpy 数组
data = tf.keras.preprocessing.image.img_to_array(img)
# 扩展维度
samples = expand_dims(data, 0)
print(samples.shape)
# 生成数据增强迭工厂
datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    rotation_range =5,    # 旋转范围#############改
    zoom_range = 0.2,   # 随机放大缩小的范围
    horizontal_flip = True,     # 水平方向翻转
    vertical_flip = False,      # 垂直方向翻转
    #rescale = 1./255,    # 标准化
    validation_split = 0.2,  # 验证集划分比例
)     # 图像增强

i=2
while(i<150):
    
    # 准备迭代器
    it = datagen.flow(samples, 
                      batch_size=1,
                      save_to_dir='./gendata/', # 图像保存
                      save_prefix=name,
                      save_format='jpg')
    # 生成数据并画图
    # 定义子图
    # pyplot.subplot(330 + 1 + i)
    # 生成一个批次图片
    batch = it.next()
    # 转换为无符号整型方便显示
    image = batch[0].astype('uint32')
    # 画图
    # pyplot.savefig('D:/college/python/myproject/thz_recg/CNN_Image_class-master/datasets/gendata/'+str(i)+'_gan.jpg')
    pyplot.imshow(image)
    pyplot.show()
    i=i+1


