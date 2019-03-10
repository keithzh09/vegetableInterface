# coding: utf-8
# @author  : lin
# @time    : 19-3-6

import os
import tensorflow as tf
from config.network_config import output_size, bp_input_size, lstm_rnn_unit
from config.network_config import lstm_input_size as input_size
from tensorflow.python.ops.rnn import dynamic_rnn
# tf.reset_default_graph()


def mkdir(path):
    """
    创建文件夹
    :param path:
    :return:
    """
    if not os.path.exists(path):
        os.makedirs(path)


def bp_network(x, keep_prob):
    """
    定义神经网络的结构
    :param x:
    :param keep_prob: 每次参与的神经元百分比
    :return:
    """
    w = tf.Variable(tf.truncated_normal([bp_input_size, 500], stddev=0.1))
    b = tf.Variable(tf.zeros([500]) + 0.1)
    re = tf.matmul(x, w) + b
    l1 = tf.nn.elu(re)  # 激活函数
    l1_drop = tf.nn.dropout(l1, keep_prob)  # keep_prob设为1则百分百的神经元工作,L1作为神经元的输出传入
    w2 = tf.Variable(tf.truncated_normal([500, 30], stddev=0.1))
    b2 = tf.Variable(tf.zeros([30]) + 0.1)
    re2 = tf.matmul(l1_drop, w2) + b2
    l2 = tf.nn.elu(re2)  # 激活函数
    l2_drop = tf.nn.dropout(l2, keep_prob)
    # w3 = tf.Variable(tf.truncated_normal([300, 30], stddev=0.1))
    # b3 = tf.Variable(tf.zeros([30]) + 0.1)
    # re3 = tf.matmul(l2_drop, w3) + b3
    # l3 = tf.nn.elu(re3)  # 激活函数
    # l3_drop = tf.nn.dropout(l3, keep_prob)
    w4 = tf.Variable(tf.random_normal([30, output_size], stddev=0.1))
    b4 = tf.Variable(tf.zeros([output_size]) + 0.1)
    prediction = tf.matmul(l2_drop, w4) + b4
    return prediction


# lstm_graph = tf.Graph()
# with lstm_graph.as_default():
#     # 输入层、输出层权重、偏置
#     weights = {
#         'in': tf.Variable(tf.random_normal([input_size, lstm_rnn_unit])),
#         'out': tf.Variable(tf.random_normal([lstm_rnn_unit, 1]))
#     }
#     biases = {
#         'in': tf.Variable(tf.constant(0.1, shape=[lstm_rnn_unit, ])),
#         'out': tf.Variable(tf.constant(0.1, shape=[1, ]))
#     }
#
#
# def lstm_network(x):
#     """
#     LSTM模型的建立
#     :param x: shape[batch_size, time_step, 输入变量个数]
#     :return:
#     """
#     # tf.reset_default_graph()
#     the_batch_size = tf.shape(x)[0]
#     the_time_step = tf.shape(x)[1]
#     w_in = weights['in']
#     b_in = biases['in']
#     # -1表示第一层靠第二层来决定, 可以说其实第一层就会编程batch_size * time_step
#
#     # g = tf.get_default_graph()
#     # print(g.get_operations())
#
#     with lstm_graph.as_default():
#         # tf.get_variable_scope().reuse_variables()
#         input_value = tf.reshape(x, [-1, input_size])  # 需要将tensor转成2维进行计算，计算后的结果作为隐藏层的输入
#         input_rnn = tf.matmul(input_value, w_in) + b_in
#         # lstm的输入格式即为[batch_size, time_step, 输入变量数目]
#         input_rnn = tf.reshape(input_rnn, [-1, the_time_step, lstm_rnn_unit])  # 将tensor转成3维，作为lstm cell的输入
#         cell = tf.nn.rnn_cell.BasicLSTMCell(lstm_rnn_unit)
#         init_state = cell.zero_state(the_batch_size, dtype=tf.float32)
#         # output_rnn是记录lstm每个输出节点的结果，final_states是最后一个cell的结果
#         output_rnn, final_states = dynamic_rnn(cell,
#                                                input_rnn, initial_state=init_state,
#                                                dtype=tf.float32)
#
#         # -1表示根据实际情况分配,比如出来的数据为100个,rnn_unit为1,则-1的位置会变为100
#         output = tf.reshape(output_rnn, [-1, lstm_rnn_unit])  # 作为输出层的输入
#         w_out = weights['out']
#         b_out = biases['out']
#         predict_value = tf.matmul(output, w_out) + b_out
#         return predict_value, final_states
#
