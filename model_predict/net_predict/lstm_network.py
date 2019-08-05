# coding: utf-8
# @author  : lin
# @time    : 19-3-10

import tensorflow as tf
import numpy as np
import time
import os
from config.network_config import lstm_input_size
from tensorflow.python.ops.rnn import dynamic_rnn
from config.network_config import lstm_model_save_path, save_file_name, batch_size, \
    train_begin, train_end, test_begin, test_end, many_days, output_size, \
    time_step, lstm_rnn_unit1, lstm_rnn_unit2, lstm_train_times

tf.reset_default_graph()


def mkdir(path):
    """
    创建文件夹
    :param path:
    :return:
    """
    if not os.path.exists(path):
        os.makedirs(path)


lstm_graph = tf.Graph()
with lstm_graph.as_default():
    # 输入层、输出层权重、偏置
    weights = {
        'in': tf.Variable(tf.random_normal([lstm_input_size, lstm_rnn_unit1])),
        'out': tf.Variable(tf.random_normal([lstm_rnn_unit2, 1]))
    }
    biases = {
        'in': tf.Variable(tf.constant(0.1, shape=[lstm_rnn_unit1, ])),
        'out': tf.Variable(tf.constant(0.1, shape=[1, ]))
    }


def lstm_network(x):
    """
    LSTM模型的建立
    :param x: shape[batch_size, time_step, 输入变量个数]
    :return:
    """
    the_batch_size = tf.shape(x)[0]
    the_time_step = tf.shape(x)[1]
    w_in = weights['in']
    b_in = biases['in']
    # -1表示第一层靠第二层来决定, 可以说其实第一层就会编程batch_size * time_step

    # tf.get_variable_scope().reuse_variables()
    with lstm_graph.as_default():
        input_value = tf.reshape(x, [-1, lstm_input_size])  # 需要将tensor转成2维进行计算，计算后的结果作为隐藏层的输入
        input_rnn = tf.matmul(input_value, w_in) + b_in
        # lstm的输入格式即为[batch_size, time_step, 输入变量数目]
        input_rnn = tf.reshape(input_rnn, [-1, the_time_step, lstm_rnn_unit1])  # 将tensor转成3维，作为lstm cell的输入
        cell1 = tf.nn.rnn_cell.BasicLSTMCell(lstm_rnn_unit1)
        cell2 = tf.contrib.rnn.BasicLSTMCell(lstm_rnn_unit2)
        cell = tf.contrib.rnn.MultiRNNCell(cells=[cell1, cell2])
        # init_state = cell.zero_state(batch_size, dtype=tf.float32)
        # output_rnn是记录lstm每个输出节点的结果，final_states是最后一个cell的结果
        output_rnn, final_states = dynamic_rnn(cell,
                                               input_rnn,  # initial_state=init_state,
                                               dtype=tf.float32)

        # -1表示根据实际情况分配,比如出来的数据为100个,rnn_unit为1,则-1的位置会变为100
        output = tf.reshape(output_rnn, [-1, lstm_rnn_unit2])  # 作为输出层的输入
        w_out = weights['out']
        b_out = biases['out']
        predict_value = tf.matmul(output, w_out) + b_out
        return predict_value, final_states


def get_train_data(price_list):
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

    return batch_index, train_x, train_y


def train_lstm(veg_id, price_list, path):
    """
    进行模型的训练以及获取准确率
    :param veg_id: 为了将命名域区分开来,方可实现多个模型的定义,保证每种蔬菜开始预测用的都是初始化的模型
    :param price_list: 价格数组
    :param path: 路径
    :return:
    """
    with lstm_graph.as_default():
        input_x = tf.placeholder(tf.float32, shape=[None, time_step, lstm_input_size])
        output_y = tf.placeholder(tf.float32, shape=[None, time_step, output_size])
        batch_index, train_x, train_y = get_train_data(price_list)

        # g = tf.get_default_graph()
        # print(g.get_operations())
        # 命名域区分开来,方可实现多个模型的定义,否则会不知道是哪个
        predict_value, _ = lstm_network(input_x)
        # 损失函数
        loss = tf.reduce_mean(tf.square(tf.reshape(predict_value, [-1]) - tf.reshape(output_y, [-1])))
        lr = tf.Variable(0.01, dtype=tf.float32)  # 学习率定义
        train_op = tf.train.AdamOptimizer(lr).minimize(loss)

        saver = tf.train.Saver()
        with tf.Session(graph=lstm_graph) as sess:
            # 初始化
            sess.run(tf.global_variables_initializer())
            # 每次以batch_size为一个批次
            for i in range(lstm_train_times):
                # 对应训练过程中出现的loss值
                loss_ = None
                sess.run(tf.assign(lr, 0.01 * 0.95 ** i))  # 逐渐下降
                for step in range(len(batch_index) - 1):
                    # 分别对应传入sess.run()的两个值
                    _, loss_ = sess.run([train_op, loss], feed_dict={
                        input_x: train_x[batch_index[step]:batch_index[step + 1]],
                        output_y: train_y[batch_index[step]:batch_index[step + 1]]})
                # 每隔100次则测试一次准确率
                if i % 100 == 0:
                    print(i, loss_)
            saver.save(sess, path)


def lstm_train(price_list, veg_id, veg_name):
    """
    训练
    :param price_list:
    :param veg_id:
    :param veg_name:
    :return:
    """
    start_time = time.time()
    path = lstm_model_save_path + veg_name
    mkdir(path)
    path += save_file_name
    train_lstm(veg_id, price_list, path)
    end_time = time.time()
    print(veg_name + ' wastes time ', end_time - start_time, ' s')
    return {"time": round(end_time - start_time, 2)}


def lstm_predict(price_list, veg_name):
    """
    预测
    :param price_list: 价格数组
    :param veg_name:
    :return:
    """

    start_time = time.time()
    path = lstm_model_save_path + veg_name + save_file_name
    # 将输入其置为二维
    price_list = [[i] for i in price_list]

    with lstm_graph.as_default():
        input_x = tf.placeholder(tf.float32, shape=[None, time_step, lstm_input_size])
        output_y = tf.placeholder(tf.float32, shape=[None, time_step, output_size])
        # 命名域区分开来,方可实现多个模型的定义,否则会不知道是哪个
        predict_value, _ = lstm_network(input_x)
        predict_price = []
        saver = tf.train.Saver()
        # 损失函数
        loss = tf.reduce_mean(tf.square(tf.reshape(predict_value, [-1]) - tf.reshape(output_y, [-1])))
        lr = tf.Variable(0.01, dtype=tf.float32)  # 学习率定义
        train_op = tf.train.AdamOptimizer(lr).minimize(loss)
        x = price_list
        with tf.Session(graph=lstm_graph) as sess:
            saver.restore(sess, path)
            for j in range(many_days):  # 滚动多少天
                predict_y = sess.run(predict_value, feed_dict={input_x: [x]})  # 要三维
                predict_y = predict_y.reshape((-1))[-1]
                predict_price.append(round(float(predict_y), 2))
                x = np.append(x[1:], [predict_y])  # 将计算值添加进去
                x = [[num] for num in x]
        end_time = time.time()
        print(veg_name + ' wastes time ', end_time - start_time, ' s')
        return predict_price


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


def get_accuracy(veg_id, price_list, path):
    """
    进行模型的训练以及获取准确率
    :param veg_id: 为了将命名域区分开来,方可实现多个模型的定义,保证每种蔬菜开始预测用的都是初始化的模型
    :param price_list: 价格数组
    :return:
    """
    with lstm_graph.as_default():
        input_x = tf.placeholder(tf.float32, shape=[None, time_step, lstm_input_size])
        output_y = tf.placeholder(tf.float32, shape=[None, time_step, output_size])
        test_x, test_y = get_test_data(price_list)

        predict_value, _ = lstm_network(input_x)
        # 损失函数
        loss = tf.reduce_mean(tf.square(tf.reshape(predict_value, [-1]) - tf.reshape(output_y, [-1])))
        lr = tf.Variable(0.01, dtype=tf.float32)  # 学习率定义
        train_op = tf.train.AdamOptimizer(lr).minimize(loss)
        saver = tf.train.Saver()
        with tf.Session(graph=lstm_graph) as sess:
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
            # 得到5%的
            num_list = (tf.cast(bool_list_5, tf.float32))
            accuracy = tf.reduce_mean(num_list)
            acc_5 = sess.run(accuracy)
            # 得到10%的
            num_list = (tf.cast(bool_list_10, tf.float32))
            accuracy = tf.reduce_mean(num_list)
            acc_10 = sess.run(accuracy)
        print(acc_1, acc_5, acc_10)
        return acc_1, acc_5, acc_10


def lstm_get_accuracy(price_list, veg_id, veg_name):
    """
    准确率
    :param price_list:
    :param veg_id:
    :param veg_name:
    :return:
    """
    path = lstm_model_save_path + veg_name
    mkdir(path)
    path += save_file_name
    acc_1, acc_5, acc_10 = get_accuracy(veg_id, price_list, path)
    acc_data = {'acc_1': round(float(acc_1), 3), 'acc_5': round(float(acc_5), 3), 'acc_10': round(float(acc_10), 3)}
    return {'data': acc_data}
