# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 21:08:59 2022

@author: 21114
"""
from skimage import io,transform
#import tensorflow as tf
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import numpy as np
import os
import glob
import matplotlib.pyplot as plt
import cv2


def get_path_a(path):                                      #得到一个文件夹里面所有的文件
    paths = []
    for root, dir, files in os.walk(path):
        for f in files:
            paths.append(os.path.join(root, f))
    return paths


# def get_path(path):
#     for x in glob.glob("./datasets/test/*.jpg"):
#         print(x)

# target_dict = {0:'necklace',1: 'phone',2:'gun'}
# w = 100
# h = 100
# c = 1

def read_one_image(path):
    img = io.imread(path)
    # io.imshow(img)
    # plt.show()
    img = transform.resize(img,(100,100,1))
    return np.asarray(img)

def recgfun(img):
    img = transform.resize(img,(100,100,1))
    target_dict = {0: 'phone',1:'gun',2:'people'}
    with tf.Session() as sess:
        data = []
        data.append(img)
        saver = tf.train.import_meta_graph('D:/college/大三上/成像/Thz_CFAR_MVWIE_master/THz_image_CNN_class-master/train_dir/mymodel.ckpt.meta')
        saver.restore(sess,tf.train.latest_checkpoint('D:/college/大三上/成像/Thz_CFAR_MVWIE_master/THz_image_CNN_class-master/train_dir/'))
    
        graph = tf.get_default_graph()
        x = graph.get_tensor_by_name("x:0")
        feed_dict = {x:data}
    
        logits = graph.get_tensor_by_name("logits_eval:0")
    
        classification_result = sess.run(logits,feed_dict)
    
        # #打印出预测矩阵
        # print(classification_result)
        # print(classification_result.shape)
        # #打印出预测矩阵每一行最大值的索引
        # print(tf.argmax(classification_result,1).eval())
        
        #根据索引通过字典对应图片的分类
        output = []
        output = tf.argmax(classification_result,1).eval()
        return target_dict[output[0]]
#%%
img = io.imread('D:/college/大三上/成像/Thz_CFAR_MVWIE_master/THz_image_CNN_class-master/thz_img/thz1.jpg')
out=recgfun(img)
print(out)








