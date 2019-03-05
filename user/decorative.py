# coding:UTF-8


"""
该模块是用户权限相关装饰器
@author: yubang
2016年10月27日
"""


from . import dao
from functools import wraps
from flask import request
import json
from lib.http_response_code import response


def check_login(fn):
    @wraps(fn)
    def _handle(*k, **v):
        user_id = dao.get_user_id_from_token(request.headers.get('token'))
        if not user_id:
            # 没有登录或则登录token已经过期
            return json.dumps(response[20102]) if user_id is 0 else json.dumps(response[20103])
        if not dao.check_user_able_access_url(user_id, request.path):
            # 没有权限
            return json.dumps(response[20203])
        return fn(*k, **v)
    return _handle
