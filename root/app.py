# coding: utf-8
# @author  : lin
# @time    : 19-2-28
from . import root_app
from flask import request
from lib.http_response_code import response
from lib.decorator import catch_error
from db_model.model_dao import UserModelDao
import json



@root_app.route('add_master', methods=['POST'])
@catch_error
def add_master():
    """
    添加管理员
    :return:
    """
    user_name = request.json['user_name']

    if user_name:
        UserModelDao.set_group_id(user_name, 2)
        #  添加成功
        response_data = response[200]
    else:
        # 缺乏参数
        response_data = response[20101]

    return json.dumps(response_data, ensure_ascii=False)


@root_app.route('delete_master', methods=['POST'])
@catch_error
def delete_master():
    """
    删除管理员
    :return:
    """
    user_name = request.json['user_name']

    if user_name:
        UserModelDao.set_group_id(user_name, 1)
        #  删除成功
        response_data = response[200]
    else:
        # 缺乏参数
        response_data = response[20101]

    return json.dumps(response_data, ensure_ascii=False)