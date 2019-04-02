# coding: utf-8
# @author  : lin
# @time    : 19-2-28

from db_model.model_dao import UserModelDao, GroupPowerModelDao
# from . import config
from config.db_config import redis_client
from lib.MD5_encrypt import md5_encrypt
from time import time
from datetime import datetime

user_id_token_key = "user_id_token_key_"  # token 与 user_id记录的redis key前缀
user_token_timeout = 3600 * 24  # token有效期
timer_token = "timer_"  # 利用redis计数器实现自增id，防止高并发下token重复


def get_user_id_from_token(token):
    """
    根据token获取用户id
    :param token: token
    :return:
    """
    if not token:
        return 0
    cache_key = user_id_token_key + token
    d = redis_client.get(cache_key)
    if d:
        # 设置过期时间
        redis_client.expire(cache_key, user_token_timeout)
    return int(d) if d else -1


def set_user_id_token(token, user_id):
    """
    记录token数据
    :param token: token
    :param user_id: 用户id
    :return:
    """
    cache_key = user_id_token_key + token
    redis_client.set(cache_key, user_id)
    # 设置超时时间
    redis_client.expire(cache_key, user_token_timeout)


def get_one_token():
    """
    随机生成一个32位的字符串
    :return:
    """
    timer_key = timer_token + datetime.now().strftime("%Y-%m-%d")
    # 自增，防止高并发下重复
    timer_id = redis_client.incr(timer_key)
    redis_client.expire(timer_key, 3600 * 24)
    d = str(time()) + "_" + str(timer_id)
    return md5_encrypt(d)


def get_user_name_from_id(user_id):
    """
    由id得name
    :param user_id:
    :return:
    """
    user = UserModelDao.find_by_user_id(user_id)
    if not (user and user.user_name):
        return None
    return user.user_name


def is_user_root(user_id):
    """
    查看一个user是否root用户
    :param user_id:
    :return:
    """
    user = UserModelDao.find_by_user_id(user_id)
    if not (user and user.group_id == 3):
        return False
    return True


def delete_one_token(token):
    cache_key = user_id_token_key + token
    redis_client.delete(cache_key)
