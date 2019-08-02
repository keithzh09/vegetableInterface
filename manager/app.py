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


@manager_app.route('get_user_data', methods=['POST'])
@catch_error
def get_user_data():
    page_size = request.json['page_size']
    page = request.json['page']
    group_id = request.json['group_id']
    all_user_list = UserModelDao.query_user(3, group_id=group_id)
    all_user_list = [i for i in all_user_list]
    user_list = all_user_list[(page - 1) * page_size: page * page_size]
    user_data = []
    for user in user_list:
        user_data.append({'user_name': user.user_name, 'user_pwd': user.user_pwd,
                          'user_state': user.user_state, 'email': user.email})
    data = {'count': len(all_user_list), 'user_data': user_data}
    return json.dumps({'code': 200, 'msg': 'Success', 'data': data})


@manager_app.route('get_user_amount', methods=['GET'])
@catch_error
def get_user_mount():
    """
    得到用户数量
    :return:
    """
    all_user_list = UserModelDao.query_user(0)
    data = {'root': 0, 'manager': 0, 'user': 0}
    for user_model in all_user_list:
        if user_model.group_id == 1:
            data['user'] += 1
        elif user_model.group_id == 2:
            data['manager'] += 1
        elif user_model.group_id == 3:
            data['root'] += 1
    response_data = {'data': data}
    response_data.update(response[200])
    return json.dumps(response_data)