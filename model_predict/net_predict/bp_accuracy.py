# coding: utf-8
# @author  : lin
# @time    : 19-3-10

import numpy as np
import tensorflow as tf
import time
import os
from config.network_config import bp_model_save_path, save_file_name, batch_size,\
    train_begin, train_end, test_begin, test_end, many_days, bp_train_times, output_size
from config.network_config import bp_input_size as input_size
from .dao import mkdir, bp_network

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # 显示warning和error

# tf.reset_default_graph()


def get_train_test_data(price_list):
    """
    得到测试的数据
    :param price_list: 价格数组
    :return:
    """
    # 获取测试数据
    data_test = price_list[test_begin:test_end]
    test_x, test_y = [], []
    for i in range(len(data_test) - input_size):
        if len(test_x) < len(data_test) - input_size - many_days:
            x = data_test[i: i + input_size]
            test_x.append(x)
        y = data_test[i + input_size]
        test_y.append([y])
    return test_x, test_y


def run(price_list, path):
    """
    开始训练网络
    :param price_list: 价格数组
    :param path: 保存网络的路径
    :return:
    """
    x = tf.placeholder(tf.float32, [None, input_size])
    y = tf.placeholder(tf.float32, [None, output_size])
    keep_prob = tf.placeholder(tf.float32)
    lf = tf.Variable(0.01, dtype=tf.float32)  # 学习率定义
    prediction = bp_network(x, keep_prob)  # 建立网络
    test_x, test_y = get_train_test_data(price_list)
    # 误差小于等于1%的准确率
    acc_1 = 0
    acc_5 = 0
    acc_10 = 0
    # 交叉熵
    loss = tf.reduce_mean(tf.square(y - prediction))
    # 梯度下降法
    train_op = tf.train.AdamOptimizer(lf).minimize(loss)
    saver = tf.train.Saver()
    with tf.Session() as sess:
        saver.restore(sess, path)
        bool_list_1 = []
        bool_list_5 = []
        bool_list_10 = []
        for step in range(len(test_x)):
            x_in = test_x[step]
            for j in range(many_days):
                predict_y = sess.run(prediction, feed_dict={x: [x_in], keep_prob: 1})  # 要三维
                predict_y = predict_y[0]
                origin_y = test_y[step + j]
                if j == many_days - 1:
                    # 获取其准确率
                    bool_list_1.append((abs(predict_y - origin_y) / origin_y < 0.01)[0])
                    bool_list_5.append((abs(predict_y - origin_y) / origin_y < 0.05)[0])
                    bool_list_10.append((abs(predict_y - origin_y) / origin_y < 0.1)[0])
                x_in = np.append(x_in[1:], predict_y)  # 将计算值添加进去
                # x = [[num] for num in x]
        # 误差小于1%的准确率
        print(len(bool_list_1))
        # cast函数将其转换为float形式
        num_list = (tf.cast(bool_list_1, tf.float32))
        # reduce_mean取平均值，此时True为1，False为0，平均值其实就是准确率
        accuracy = tf.reduce_mean(num_list)
        acc_1 = sess.run(accuracy)
        print(acc_1)
        num_list = (tf.cast(bool_list_5, tf.float32))
        accuracy = tf.reduce_mean(num_list)
        acc_5 = sess.run(accuracy)
        print(acc_5)
        num_list = (tf.cast(bool_list_10, tf.float32))
        accuracy = tf.reduce_mean(num_list)
        acc_10 = sess.run(accuracy)
        print(acc_10)
    return acc_1, acc_5, acc_10


def training(price_list, veg_name):
    """
    入口
    :param price_list:
    :param veg_name:蔬菜名
    :return:
    """
    # 详细解释看train_bp函数

    path = bp_model_save_path + veg_name
    mkdir(path)
    path += save_file_name
    acc_1, acc_5, acc_10 = run(price_list, path)
    acc_data = {'acc_1': round(float(acc_1), 3), 'acc_5': round(float(acc_5), 3), 'acc_10': round(float(acc_10), 3)}
    return acc_data


def bp_get_accuracy(price_list, veg_name):
    start_time = time.time()
    acc_data = training(price_list, veg_name)
    end_time = time.time()
    print(veg_name + ' wastes time ', end_time - start_time, ' s')
    return {"acc_data": acc_data, "time": round(end_time-start_time, 2)}
