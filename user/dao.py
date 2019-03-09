# coding: utf-8
# @author  : lin
# @time    : 19-2-28
from threading import Thread

from db_model.model_dao import UserModelDao, GroupPowerModelDao
# from . import config
from config.db_config import redis_client
from lib.MD5_encrypt import md5_encrypt
from time import time
from datetime import datetime
import re
from flask_mail import Mail, Message
from http_apis import app
import random

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


def check_user_able_access_url(user_id, url):
    """
    判断用户是否可以访问某url
    :param user_id: 用户id
    :param url: api地址
    :return:
    """
    # 检查用户所属用户组
    user = UserModelDao.find_by_user_id(user_id)
    if not (user and user.group_id):
        return False

    # # 检查用户组是否存在
    # if not UserGroupModelDao.find_by_id(user.group_id):
    #     return False

    # 检查权限
    return GroupPowerModelDao.check_group_permission(user.group_id, url)


def send_email(msg):
    """
    发送邮件
    :param msg: 存储要发送信息的Message类
    :return:
    """
    with app.app_context():
        mail = Mail(app)
        mail.send(msg)


# 验证邮箱格式
def validate_email(email):
    """
    检验邮箱格式是否正确
    :param email: 邮箱地址
    :return:
    """
    if len(email) > 7:
        if not re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) is None:
            return 1
    return 0


def thread_send_email(email):
    email_code = ''.join(str(i) for i in random.sample(range(0, 9), 4))  # 生成4位随机验证码
    msg = Message('注册验证码', sender='434345158@qq.com', recipients=[email])
    msg.body = "您的注册验证码为" + email_code
    thread = Thread(target=send_email, args=[msg])  # 开启另一线程执行发邮件功能
    thread.start()
    return email_code
