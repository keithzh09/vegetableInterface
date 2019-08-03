# coding: utf-8
# @author  : lin
# @time    : 19-2-28
from threading import Thread

from db_model.model_dao import UserModelDao, GroupPowerModelDao, VegetableModelDao, VegetablePriceModelDao
# from . import config
from config.db_config import redis_client
from lib.MD5_encrypt import md5_encrypt
from lib.dao import get_user_id_from_token, set_user_id_token, get_one_token
import re
from flask_mail import Mail, Message
from http_apis import app
import random


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


def get_today_price(today_time):
    data = redis_client.get('REDIS_TODAY_VEG_PRICE' + today_time)
    if not data:
        data = []
        veg_model_list = VegetablePriceModelDao.query_vegetable_price_data(5, start_date=today_time)
        for veg_model in veg_model_list:
            veg_name = VegetableModelDao.get_name_by_id(veg_model.veg_id)
            one_price = [veg_name, veg_model.date, veg_model.price, veg_model.place]
            data.append(one_price)
        if len(data) > 0:
            redis_client.set('REDIS_TODAY_VEG_PRICE' + today_time, str(data))
            # 设置过期时间
            redis_client.expire('REDIS_TODAY_VEG_PRICE' + today_time, 3600*24)
    else:
        data = eval(data)
    return data

