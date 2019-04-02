# coding: utf-8
# @author  : lin
# @time    : 19-2-28
from . import dao
from flask import request, Blueprint
from lib.http_response_code import response
from lib.decorator import catch_error
from db_model.model_dao import UserModelDao
import json

root_app = Blueprint('root_app', __name__)


@root_app.route('add_manager', methods=['POST'])
@catch_error
def add_manager():
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


@root_app.route('delete_manager', methods=['POST'])
@catch_error
def delete_manager():
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


@root_app.route('get_info', methods=['GET'])
@catch_error
def get_user_info():
    token = request.headers.get('token')
    user_id = dao.get_user_id_from_token(token)
    print(user_id)
    user_name = dao.get_user_name_from_id(user_id)
    # uid =
    res = {
        'avator': 'ME',   # 头像
        'name': user_name,
        'user_id': user_id,
        'access': ['super_admin']
    }
    return json.dumps({'code': 200, 'msg': 'Success', 'data': res})


@root_app.route('login', methods=['POST'])
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
    if not dao.is_user_root(user_id):
        # 校验不通过
        return json.dumps(response[20201]) if user_id == -1 else json.dumps(response[20202])

    token = dao.get_one_token()
    dao.set_user_id_token(token, user_id)
    response_data = {"token": token, 'user_id': user_id}
    response_data.update(response[200])
    return json.dumps(response_data)


@root_app.route('logout', methods=['POST'])
@catch_error
def user_logout():
    """
    取消掉token
    :return:
    """
    token = request.headers.get('token')
    dao.delete_one_token(token)
    user_id = dao.get_user_id_from_token(token)
    return json.dumps(response[200])


@root_app.route('get_user_mount', methods=['GET'])
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


@root_app.route('get_user_data', methods=['POST'])
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


@root_app.route('get_user_ui', methods=['GET'])
@catch_error
def return_ui_config():
    columns = UserModelDao.get_ui_config()
    return json.dumps({'code': 200, 'msg': 'Success', 'data': columns})
