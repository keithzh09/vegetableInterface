# coding: utf-8
# @author  : lin
# @time    : 19-3-7


"""
这个文件主要做的工作：
    1. 根据蔬菜名创建该保存模型的路径的目录（不存在时）
    2. 训练模型，保存网络
"""

import numpy as np
import tensorflow as tf
import time
import os
from config.network_config import lstm_model_save_path, save_file_name, batch_size,\
    train_begin, train_end, test_begin, test_end, many_days, bp_train_times, output_size,\
    time_step, lstm_rnn_unit, lstm_train_times
from config.network_config import lstm_input_size as input_size
from .dao import mkdir, lstm_network
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # 显示warning和error


def get_train_test_data(price_list):
    """
    得到训练和测试的数据
    :param price_list: 价格数组
    :return:
    """
    # 获取训练数据
    batch_index = []  # 得到每两个批次间的下标
    data_train = np.array(price_list[train_begin:train_end])
    train_x, train_y = [], []  # 训练集
    for i in range(len(data_train) - time_step):
        if i % batch_size == 0:  # 每隔一个批次添加一下下表
            batch_index.append(i)
        x = data_train[i:i + time_step, np.newaxis]  # np.newaxis为array增加一维
        y = data_train[i + 1:i + time_step + 1, np.newaxis]
        train_x.append(x.tolist())
        train_y.append(y.tolist())
    batch_index.append((len(data_train) - time_step))

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
    return batch_index, train_x, train_y, test_x, test_y


def train_lstm(veg_id, price_list, path):
    """
    进行模型的训练以及获取准确率
    :param veg_id: 为了将命名域区分开来,方可实现多个模型的定义,保证每种蔬菜开始预测用的都是初始化的模型
    :param price_list: 价格数组
    :return:
    """
    input_x = tf.placeholder(tf.float32, shape=[None, time_step, input_size])
    output_y = tf.placeholder(tf.float32, shape=[None, time_step, output_size])
    batch_index, train_x, train_y, test_x, test_y = get_train_test_data(price_list)
    # 命名域区分开来,方可实现多个模型的定义,否则会不知道是哪个
    with tf.variable_scope(veg_id):
        predict_value, _ = lstm_network(input_x)
    acc_1 = 0
    acc_5 = 0
    acc_10 = 0
    # 损失函数
    loss = tf.reduce_mean(tf.square(tf.reshape(predict_value, [-1]) - tf.reshape(output_y, [-1])))
    lr = tf.Variable(0.01, dtype=tf.float32)  # 学习率定义
    train_op = tf.train.AdamOptimizer(lr).minimize(loss)
    saver = tf.train.Saver()
    with tf.Session() as sess:
        # 初始化
        sess.run(tf.global_variables_initializer())
        # 每次以batch_size为一个批次
        for i in range(lstm_train_times):
            # 对应训练过程中出现的loss值
            loss_ = None
            sess.run(tf.assign(lr, 0.01 * 0.95 ** i))     # 逐渐下降
            for step in range(len(batch_index) - 1):
                # 分别对应传入sess.run()的两个值
                _, loss_ = sess.run([train_op, loss], feed_dict={
                    input_x: train_x[batch_index[step]:batch_index[step + 1]],
                    output_y: train_y[batch_index[step]:batch_index[step + 1]]})
            # 每隔100次则测试一次准确率
            if i % 100 == 0:
                print(i, loss_)
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
        saver.save(sess, path)
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
    acc_data = {'acc_1': acc_1, 'acc_5': acc_5, 'acc_10': acc_10}
    return acc_data


def lstm_train(price_list, veg_id, veg_name):
    start_time = time.time()
    acc_data = training(price_list, veg_id, veg_name)
    end_time = time.time()
    print(veg_name + ' wastes time ', end_time - start_time, ' s')
    return {"acc_data": acc_data, "time": end_time-start_time}

