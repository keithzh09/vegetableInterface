# coding: utf-8
# @author  : lin
# @time    : 19-2-28

from flask import Blueprint, request, make_response
from . import dao
from db_model.model_dao import UserModelDao, VegetableModelDao, VegetablePriceModelDao
import json
from lib.http_response_code import response
from lib.decorator import catch_error
import peewee
user_app = Blueprint("user_app", __name__)


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


