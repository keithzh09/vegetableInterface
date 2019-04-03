from traceback import format_tb
from functools import wraps
from flask import make_response, request, Response
from lib.http_response_code import response
from lib import dao
import json
from lib.url_params import params
from db_model.model_dao import GroupPowerModelDao, UserModelDao

def catch_error(func):
    @wraps(func)
    def _handle(*k, **v):
        try:
            # resp = make_response(func(*k, **v))
            # resp.headers['Access-Control-Allow-Origin'] = '*'
            # resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
            # resp.headers['Access-Control-Allow-Headers'] = 'token,Referer,Accept,Origin,User-Agent,content-type'
            return func(*k, **v)
        except Exception as error:
            print(format_tb(error.__traceback__), type(error), error)
            resp = Response(json.dumps(response[-200]))
            resp = Response(json.dumps(error))
            # resp.headers['Access-Control-Allow-Origin'] = '*'
            # resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
            # resp.headers['Access-Control-Allow-Headers'] = 'token'
            return resp
    return _handle


def check_url_params(func):
    @wraps(func)
    def _handle(*k, **v):
        req_json = eval(request.get_data())
        url = request.path
        url_params = params[url]
        for param in url_params:
            if param not in req_json.keys():
                return json.dumps(response[20101])
        return func(*k, **v)
    return _handle


def check_user_permission(func):
    @wraps(func)
    def _handle(*k, **v):
        token = request.headers.get('token')
        user_id = dao.get_user_id_from_token(token)
        user = UserModelDao.find_by_user_id(user_id)
        if not (user and user.group_id):  # 不存在
            return json.dumps(response[20201])
        url = request.path
        print(url)
        if not GroupPowerModelDao.check_group_permission(user.group_id, url):
            return json.dumps(response[20203])  # 无权限
        return func(*k, **v)
    return _handle

