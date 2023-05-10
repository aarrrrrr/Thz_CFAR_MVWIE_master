from skimage import io,transform
#import tensorflow as tf
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import numpy as np
import os
import glob
import matplotlib.pyplot as plt


def get_path_a(path):                                      #得到一个文件夹里面所有的文件
    paths = []
    for root, dir, files in os.walk(path):
        for f in files:
            paths.append(os.path.join(root, f))
    return paths


# def get_path(path):
#     for x in glob.glob("./datasets/test/*.jpg"):
#         print(x)


target_dict = {0: 'phone',1:'gun',2:'people'}
w = 100
h = 100
c = 1


def read_one_image(path):
    img = io.imread(path)
    # io.imshow(img)
    # plt.show()
    img = transform.resize(img,(w,h,c))
    return np.asarray(img)


with tf.Session() as sess:
    data = []
    paths = get_path_a("./datasets/test/")
    for p in paths:
        data.append(read_one_image(p))
    saver = tf.train.import_meta_graph('./train_dir/mymodel.ckpt.meta')
    saver.restore(sess,tf.train.latest_checkpoint('./train_dir/'))

    graph = tf.get_default_graph()
    x = graph.get_tensor_by_name("x:0")
    feed_dict = {x:data}

    logits = graph.get_tensor_by_name("logits_eval:0")

    classification_result = sess.run(logits,feed_dict)


    #打印出预测矩阵
    print(classification_result)
    print(classification_result.shape)
    #打印出预测矩阵每一行最大值的索引
    print(tf.argmax(classification_result,1).eval())
    #根据索引通过字典对应图片的分类
    output = []
    output = tf.argmax(classification_result,1).eval()
    for i in range(len(output)):
        print(paths[i]+"识别结果:"+target_dict[output[i]])