# coding: utf-8
# @author  : lin
# @time    : 19-3-7
import tensorflow as tf
import time
import os
import numpy as np

from config.network_config import lstm_model_save_path, save_file_name, lstm_input_size,\
    many_days, output_size, time_step
from .dao import lstm_network, lstm_graph
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def predict(veg_id, price_list, path):
    """
    预测
    :param veg_id: 蔬菜id
    :param price_list: 价格数组
    :param path: 存放路径
    :return:
    """
    with lstm_graph.as_default():
        input_x = tf.placeholder(tf.float32, shape=[None, time_step, lstm_input_size])
        output_y = tf.placeholder(tf.float32, shape=[None, time_step, output_size])
        # 命名域区分开来,方可实现多个模型的定义,否则会不知道是哪个
        with tf.variable_scope(str(veg_id)):
            predict_value, _ = lstm_network(input_x)
        predict_price = []
        saver = tf.train.Saver()
        # 损失函数
        loss = tf.reduce_mean(tf.square(tf.reshape(predict_value, [-1]) - tf.reshape(output_y, [-1])))
        lr = tf.Variable(0.01, dtype=tf.float32)  # 学习率定义
        train_op = tf.train.AdamOptimizer(lr).minimize(loss)
        x = price_list
        with tf.Session() as sess:
            tf.get_variable_scope().reuse_variables()
            saver.restore(sess, path)
            for j in range(many_days):  # 滚动多少天
                predict_y = sess.run(predict_value, feed_dict={input_x: [x]})  # 要三维
                predict_y = predict_y.reshape((-1))[-1]
                predict_price.append(round(float(predict_y), 2))
                x = np.append(x[1:], [predict_y])  # 将计算值添加进去
                x = [[num] for num in x]
        return predict_price


def lstm_predict(price_list, veg_id, veg_name):
    start_time = time.time()
    path = lstm_model_save_path + veg_name + save_file_name
    print(path)
    # 将输入其置为二维
    price_list = [[i] for i in price_list]
    predict_price = predict(veg_id, price_list, path)
    end_time = time.time()
    print(veg_name + ' wastes time ', end_time - start_time, ' s')
    return predict_price
