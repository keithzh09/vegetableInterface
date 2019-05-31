# coding: utf-8
# @author  : lin
# @time    : 19-2-28

from db_model.model_dao import UserModelDao, GroupPowerModelDao
# from . import config
from config.db_config import redis_client
from lib.MD5_encrypt import md5_encrypt
from time import time
from datetime import datetime


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


