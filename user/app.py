# coding: utf-8
# @author  : lin
# @time    : 19-2-28

from flask import request
from flask_mail import Message
from . import dao
from db_model.model_dao import UserModelDao, VegetableModelDao, VegetablePriceModelDao
import json
from lib.http_response_code import response
from lib.decorator import catch_error
import re
import random
from threading import Thread
from . import user_app


@user_app.route('', methods=['GET'])
@catch_error
def index():
    return "hello"


@user_app.route('login', methods=['POST'])
@catch_error
def user_login():
    """
    获取api调用token
    :return:
    """
    # 测试用户：test_user,密码：TestUser_Key
    req_json = request.json
    user_name = req_json["user_name"]
    user_pwd = req_json["user_pwd"]

    if not (user_name and user_pwd):
        # 参数缺失
        return json.dumps(response[20101])

    user_id = UserModelDao.check_user_and_user_pwd(user_name, user_pwd)
    if user_id <= 0:
        # 校验不通过
        return json.dumps(response[20201]) if user_id == -1 else json.dumps(response[20202])

    token = dao.get_one_token()
    dao.set_user_id_token(token, user_id)
    response_data = {"token": token, 'user_id': user_id}
    response_data.update(response[200])
    return json.dumps(response_data)


email_code = ''


@user_app.route("/register", methods=['POST'])
@catch_error
def register():
    """
    用户注册功能
    :return:
    """
    global email_code
    data = request.get_json()  # 获取表单数据
    name = data.get("user_name")
    pwd = data.get("password")
    check_pwd = data.get("check_password")
    email = data.get("email")
    user_email_code = data.get("email_code")

    if name and pwd and email and user_email_code and check_pwd:
        if not re.search(u'^[_a-zA-Z0-9\u4e00-\u9fa5]+$', name):
            # 用户名格式出错
            dict_info = response[20302]
        elif UserModelDao.query_user(1, user_name=name):
            # 用户名已存在
            dict_info = response[20301]
        elif len(pwd) < 6:
            # 密码长度太短
            dict_info = response[20303]
        elif check_pwd != pwd:
            # 两次密码输入不一致
            dict_info = response[20304]
        elif user_email_code != email_code:
            # 邮箱验证码错误
            dict_info = response[20305]
        else:
            # 插入新用户
            UserModelDao.add_user(name, pwd, email)
            dict_info = response[200]
    else:
        # 缺少参数
        dict_info = response[20101]

    return json.dumps(dict_info, ensure_ascii=False)


# 验证邮箱格式正确性，正确则发送邮箱
@user_app.route("register/send_email", methods=['POST'])
@catch_error
def send_email():
    """
    开启另一个线程发送邮箱验证码
    :return:
    """
    global email_code
    email = request.json["email"]  # 获取用户输入的邮箱

    if dao.validate_email(email):  # 检验邮箱格式
        if UserModelDao.query_user(3, email=email):
            # 邮箱已被使用
            dict_info = response[20306]
        else:
            email_code = ''.join(str(i) for i in random.sample(range(0, 9), 4))  # 生成4位随机验证码
            msg = Message('注册验证码', sender='434345158@qq.com', recipients=[email])
            msg.body = "您的注册验证码为" + email_code
            thread = Thread(target=dao.send_async_email, args=[msg])  # 开启另一线程执行发邮件功能
            thread.start()
            # 发送成功z
            dict_info = response[200]
    else:
        # 缺少参数
        dict_info = response[20307]

    return json.dumps(dict_info, ensure_ascii=False)


@user_app.route('vegetable/k_line', methods=['POST'])
@catch_error
def get_k_line():
    """
    获取蔬菜k线图
    :return:
    """
    req_json = request.json
    vegetable_name = req_json['vegetable_name']
    date = req_json['date']

    if not (vegetable_name and date):
        return json.dumps(response[20101])
    price = []
    new_date = []
    for veg_name in vegetable_name:
        veg_id = VegetableModelDao.get_id_by_name(veg_name)
        veg_model_list = VegetablePriceModelDao.query_vegetable_price_data(2, veg_id, date[0], date[1])
        price.append([veg_model.price for veg_model in veg_model_list])
        new_date.append([veg_model.date for veg_model in veg_model_list])

    response_data = {'vegetable_name': vegetable_name, 'price': price, 'date': new_date}
    response_data.update(response[200])
    return json.dumps(response_data)


