# coding: utf-8
# @author  : lin
# @time    : 19-2-28
import re
import json

from flask import request
from . import dao
from db_model.model_dao import UserModelDao, VegetableModelDao, VegetablePriceModelDao, PredictModelModelDao
from lib.http_response_code import response
from lib.decorator import catch_error
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


register_email_code = ''


@user_app.route("register", methods=['POST'])
@catch_error
def register():
    """
    用户注册功能
    :return:
    """
    global register_email_code
    data = request.json  # 获取表单数据
    name = data["user_name"]
    pwd = data["password"]
    check_pwd = data["check_password"]
    email = data["email"]
    user_email_code = data["email_code"]

    if name and pwd and email and user_email_code and check_pwd:
        if not re.search(u'^[_a-zA-Z0-9\u4e00-\u9fa5]+$', name):
            # 用户名格式出错
            response_data = response[20302]
        elif UserModelDao.query_user(1, user_name=name):
            # 用户名已存在
            response_data = response[20301]
        elif len(pwd) < 6:
            # 密码长度太短
            response_data = response[20303]
        elif check_pwd != pwd:
            # 两次密码输入不一致
            response_data = response[20304]
        elif user_email_code != register_email_code:
            # 邮箱验证码错误
            response_data = response[20305]
        else:
            # 插入新用户
            UserModelDao.add_user(name, pwd, email)
            response_data = response[200]
    else:
        # 缺少参数
        response_data = response[20101]

    return json.dumps(response_data, ensure_ascii=False)


# 验证邮箱格式正确性，正确则发送邮箱
@user_app.route("register/send_email", methods=['POST'])
@catch_error
def register_send_email():
    """
    注册时，开启另一个线程发送邮箱验证码
    :return:
    """
    global register_email_code
    email = request.json["email"]  # 获取用户输入的邮箱

    if email:
        if not dao.validate_email(email):
            # 邮箱格式错误
            response_data = response[20307]
        elif UserModelDao.query_user(3, email=email):
            # 邮箱已被使用
            response_data = response[20306]
        else:
            register_email_code = dao.thread_send_email(email)
            print(register_email_code)
            # 发送成功
            response_data = response[200]
    else:
        # 缺少参数
        response_data = response[20101]

    return json.dumps(response_data, ensure_ascii=False)


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
    veg_id = VegetableModelDao.get_id_by_name(vegetable_name)
    veg_model_list = VegetablePriceModelDao.query_vegetable_price_data(2, veg_id, date[0], date[1])
    for veg_model in veg_model_list:
        one_price = [vegetable_name, veg_model.date, veg_model.price, veg_model.place]
        price.append(one_price)

    response_data = {'vegetable_name': vegetable_name, 'data': price}
    response_data.update(response[200])
    return json.dumps(response_data)


alter_email_code = ''


@user_app.route('alter_pwd', methods=['POST'])
@catch_error
def alter_pwd():
    """
    用户修改密码
    :return:
    """
    global alter_email_code
    req_json = request.json
    user_name = req_json['user_name']
    new_password = req_json['new_password']
    re_password = req_json['re_password']
    email = req_json['email']
    user_email_code = req_json['email_code']

    if user_name and new_password and re_password and email and user_email_code:
        if not UserModelDao.query_user(1, user_name=user_name):
            # 用户名不存在
            response_data = response[20201]
        elif new_password != re_password:
            # 两次输入密码不一致
            response_data = response[20304]
        elif user_email_code != alter_email_code:
            # 邮箱验证码错误
            response_data = response[20305]
        else:
            # 修改成功
            UserModelDao.alter_user_pwd(user_name, new_password)
            response_data = response[200]
    else:
        # 缺少参数
        response_data = response[20101]

    return json.dumps(response_data, ensure_ascii=False)


@user_app.route('alter_pwd/send_email', methods=['POST'])
@catch_error
def alter_send_email():
    """
    修改密码时，开启另一个线程发送邮箱验证码
    :return:
    """
    global alter_email_code
    email = request.json['email']
    user_name = request.json['user_name']

    if email and user_name:
        if not dao.validate_email(email):
            # 邮箱格式错误
            response_data = response[20307]
        elif not UserModelDao.query_user(4, user_name=user_name, email=email):
            # 用户名和邮箱不匹配
            response_data = response[20308]
        else:
            alter_email_code = dao.thread_send_email(email)
            # 发送成功
            response_data = response[200]
    else:
        # 缺少参数
        response_data = response[20101]

    return json.dumps(response_data, ensure_ascii=False)


@user_app.route('vegetable/information', methods=['POST'])
@catch_error
def vegetable_info():
    """
    获取蔬菜信息
    :return:
    """
    vegetable_name = request.json['vegetable_name']
    if vegetable_name:
        if VegetableModelDao.get_id_by_name(vegetable_name):
            vegetable_information = VegetableModelDao.get_information(vegetable_name)
            if vegetable_information is None:
                # 无蔬菜信息
                response_data = response[20503]
            else:
                # 获取信息成功
                response_data = {'vegetable_info': vegetable_information}
                response_data.update(response[200])
        else:
            # 缺少蔬菜
            response_data = response[20401]
    else:
        # 缺少参数
        response_data = response[20101]
    return json.dumps(response_data, ensure_ascii=False)


@user_app.route('vegetable/get_all_vegetables', methods=['GET'])
@catch_error
def all_vegetable():
    """
    获取所有蔬菜
    :return:
    """
    data = []
    vegetable_list = VegetableModelDao.query_vegetable()
    for i in range(len(vegetable_list)):
        vegetable = vegetable_list[i]
        one_data_1 = {'name': vegetable.veg_name, 'img_url': vegetable.veg_img_url,
                      'description': vegetable.veg_information}
#        one_data = {str(i + 1): one_data_1}
        data.append(one_data_1)
    response_data = {'data': data}
    response_data.update(response[200])
    return json.dumps(response_data, ensure_ascii=False)
