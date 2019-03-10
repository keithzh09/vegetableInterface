# coding: utf-8
# @author  : lin
# @time    : 19-3-10

import numpy as np
import tensorflow as tf
import time
import os
from config.network_config import lstm_model_save_path, save_file_name, batch_size,\
    train_begin, train_end, test_begin, test_end, many_days, bp_train_times, output_size,\
    time_step, lstm_rnn_unit, lstm_train_times
from config.network_config import lstm_input_size as input_size
from .dao import mkdir, lstm_network, lstm_graph
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # 显示warning和error


def get_test_data(price_list):
    """
    得到测试的数据
    :param price_list: 价格数组
    :return:
    """
    # 获取测试数据
    data_test = np.array(price_list[test_begin: test_end])
    # mean = np.mean(data_test, axis=0)
    # std = np.std(data_test, axis=0)
    test_x, test_y = [], []
    for i in range(len(data_test) - time_step):
        # test_y应该至少多出many_days个长度，才可进行滚动预测
        if len(test_x) < (len(data_test) - many_days - time_step):
            x = data_test[i:i + time_step, np.newaxis]
            test_x.append(x.tolist())
        y = data_test[i + time_step]
        test_y.append(y)
    test_y = [[i] for i in test_y]
    return test_x, test_y


def train_lstm(veg_id, price_list, path):
    """
    进行模型的训练以及获取准确率
    :param veg_id: 为了将命名域区分开来,方可实现多个模型的定义,保证每种蔬菜开始预测用的都是初始化的模型
    :param price_list: 价格数组
    :return:
    """
    # tf.reset_default_graph()

    with lstm_graph.as_default():
        input_x = tf.placeholder(tf.float32, shape=[None, time_step, input_size])
        output_y = tf.placeholder(tf.float32, shape=[None, time_step, output_size])
        test_x, test_y = get_test_data(price_list)

        with tf.variable_scope(str(veg_id)):
            predict_value, _ = lstm_network(input_x)
        # 损失函数
        loss = tf.reduce_mean(tf.square(tf.reshape(predict_value, [-1]) - tf.reshape(output_y, [-1])))
        lr = tf.Variable(0.01, dtype=tf.float32)  # 学习率定义
        train_op = tf.train.AdamOptimizer(lr).minimize(loss)
        saver = tf.train.Saver()
        with tf.Session() as sess:
            # 初始化
            saver.restore(sess, path)
            tf.get_variable_scope().reuse_variables()

            test_predict = []
            bool_list_1 = []
            bool_list_5 = []
            bool_list_10 = []
            for step in range(len(test_x)):
                x = test_x[step]
                # prob代表投入数据预测得到的结果
                prob = None
                # 接下来是滚动预测了
                for j in range(many_days):
                    # 输入要三维
                    prob = sess.run(predict_value, feed_dict={input_x: [x]})
                    # 先把输出可能多维的情况，转换成一维
                    predict = prob.reshape((-1))
                    # 最后一个便是预测对应y的那一天
                    predict_y = predict[-1]
                    origin_y = test_y[step + j]
                    # 当滚动预测到了最后一天了
                    if j == many_days - 1:
                        # 之所以后面需要加个[0]就是因为predict_y和origin_y都是数组，虽然只有一个数
                        bool_list_1.append((abs(predict_y - origin_y) / origin_y < 0.01)[0])
                        bool_list_5.append((abs(predict_y - origin_y) / origin_y < 0.05)[0])
                        bool_list_10.append((abs(predict_y - origin_y) / origin_y < 0.1)[0])
                    # 重置输入x，将预测得到的值加进去，并去掉原来的第一个数
                    x = np.append(x[1:], [predict_y])  # 将计算值添加进去
                    x = [[num] for num in x]
                predict = prob.reshape((-1))
                test_predict.extend(predict)
            # 得到误差小于1%的准确率了，tf.cast将值转换为float格式
            num_list = (tf.cast(bool_list_1, tf.float32))
            # reduce_mean得到平均值，此时True已经为1，False已经为0，故平均值就是准确率
            accuracy = tf.reduce_mean(num_list)
            acc_1 = sess.run(accuracy)
            print(acc_1)
            # 得到5%的
            num_list = (tf.cast(bool_list_5, tf.float32))
            accuracy = tf.reduce_mean(num_list)
            acc_5 = sess.run(accuracy)
            print(acc_5)
            # 得到10%的
            num_list = (tf.cast(bool_list_10, tf.float32))
            accuracy = tf.reduce_mean(num_list)
            acc_10 = sess.run(accuracy)
            print(acc_10)
        return acc_1, acc_5, acc_10


def training(price_list, veg_id, veg_name):
    """
    入口
    :param price_list:
    :param veg_id: 蔬菜id
    :param veg_name: 蔬菜名
    :return:
    """
    # 详细解释看train_bp函数

    path = lstm_model_save_path + veg_name
    mkdir(path)
    path += save_file_name
    acc_1, acc_5, acc_10 = train_lstm(veg_id, price_list, path)
    acc_data = {'acc_1': round(float(acc_1), 3), 'acc_5': round(float(acc_5), 3), 'acc_10': round(float(acc_10), 3)}
    return acc_data


def lstm_get_accuracy(price_list, veg_id, veg_name):
    start_time = time.time()
    acc_data = training(price_list, veg_id, veg_name)
    end_time = time.time()
    print(veg_name + ' wastes time ', end_time - start_time, ' s')
    return {"acc_data": acc_data, "time": round(end_time-start_time, 2)}

