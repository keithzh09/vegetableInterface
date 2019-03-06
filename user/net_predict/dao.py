# coding: utf-8
# @author  : lin
# @time    : 19-3-6

import os
import tensorflow as tf
from config.network_config import output_size, bp_input_size


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

