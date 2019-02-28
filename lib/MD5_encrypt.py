# coding: utf-8
# @author: lin
# @date: 19-02-28


"""
MD5加密调用函数
@author: Ulysses_Xu
创建于2017年9月9日
"""
import hashlib


def md5_encrypt(data):
    m = hashlib.md5()
    m.update(data.encode('UTF-8'))
    return m.hexdigest()
