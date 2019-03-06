# coding: utf-8
# @author  : lin
# @time    : 19-2-28
from . import manager_app
from lib.decorator import catch_error
from flask import request
import json
from db_model.model_dao import VegetableModelDao,UserModelDao
from lib.http_response_code import response

@manager_app.route('')
@catch_error
def index():
    return 'hello'


@manager_app.route('alter_vegetable', methods=['POST'])
@catch_error
def alter_vegetable():
    """
    增添蔬菜信息
    :return:
    """
    veg_name = request.json["vegetable_name"]
    veg_information = request.json["vegetable_information"]
    operate_type = request.json["operate_type"]
    print(operate_type)

    if veg_name and operate_type is not None:
        if operate_type is True:
            if veg_information:
                for i in range(len(veg_name)):
                    VegetableModelDao.add_vegetable(veg_name[i], veg_information[i])
                # 添加成功
                response_data = response[200]
            else:
                 # 缺少参数
                 response_data = response[20101]
        else:
            for i in range(len(veg_name)):
                VegetableModelDao.delete_vegetable(veg_name[i])
            # 删除成功
            response_data = response[200]
    else:
        # 缺少参数
        response_data = response[20101]

    return json.dumps(response_data, ensure_ascii=False)


@manager_app.route('set_user_state', methods=['POST'])
@catch_error
def set_user_state():
    """
    设置用户状态，禁用或者恢复用户
    :return:
    """
    user_name = request.json["user_name"]
    user_state = request.json["user_state"]

    if user_name and user_state is not None:
        UserModelDao.set_user_state(user_name, user_state)
        # 设置成功
        response_data = response[200]
    else:
        # 参数缺乏
        response_data = response[20101]

    return json.dumps(response_data, ensure_ascii=False)


