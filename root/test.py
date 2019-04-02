# coding: utf-8
# @author  : lin
# @time    : 19-3-27

from db_model.model_dao import UserModelDao, GroupPowerModelDao
import json


def get_user_data():
    page_size = 10
    page = 1

    all_user = UserModelDao.query_user(0)
    all_list = [i for i in all_user]
    data = all_list[(page-1)*page_size: page*page_size]
    user_name = []
    user_pwd = []
    state = []
    email = []
    for i in data:
        user_name.append(i.user_name)
        user_pwd.append(i.user_pwd)
        state.append(i.user_state)
        email.append(i.email)
    print(user_name, user_pwd, email, state)
    return json.dumps({'code': 200, 'msg': 'Success', 'data': {'user_name': user_name, 'user_pwd': user_pwd,
                                                               'email': email}})


# print(get_user_data())


