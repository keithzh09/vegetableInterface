# coding: utf-8
# @author  : lin
# @time    : 19-3-5
import tensorflow as tf
import time
import os

from config.network_config import bp_model_save_path, save_file_name, bp_input_size,\
    many_days, output_size
from .dao import bp_network
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def predict(price_list, path):
    """
    预测
    :param price_list: 价格数组
    :param path: 存放路径
    :return:
    """
    x = tf.placeholder(tf.float32, [None, bp_input_size])
    y = tf.placeholder(tf.float32, [None, output_size])
    keep_prob = tf.placeholder(tf.float32)
    lf = tf.Variable(0.01, dtype=tf.float32)  # 学习率定义
    prediction = bp_network(x, keep_prob)  # 建立网络
    saver = tf.train.Saver()
    predict_price = []
    # 交叉熵
    loss = tf.reduce_mean(tf.square(y - prediction))
    # 梯度下降法
    train_op = tf.train.AdamOptimizer(lf).minimize(loss)
    with tf.Session() as sess:
        tf.get_variable_scope().reuse_variables()
        saver.restore(sess, path)
        for j in range(many_days):
            predict_y = sess.run(prediction, feed_dict={x: [price_list], keep_prob: 1})  # 要三维
            predict_price.append(predict_y[0][0])
    return predict_price


def bp_predict(price_list, veg_name):
    start_time = time.time()
    path = bp_model_save_path + veg_name + save_file_name
    print(path)
    predict_price = predict(price_list, path)
    end_time = time.time()
    print(veg_name + ' wastes time ', end_time - start_time, ' s')
    return predict_price
