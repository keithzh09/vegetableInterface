from traceback import format_tb
from functools import wraps
from flask import make_response, request, Response
from lib.http_response_code import response
import json
from lib.url_params import params


def catch_error(func):
    @wraps(func)
    def _handle(*k, **v):
        """
        error装饰器
        :param k:
        :param v:
        :return:
        """
        try:
            return func(*k, **v)
        except Exception as error:
            print(format_tb(error.__traceback__), type(error), error)
            resp = Response(json.dumps(response[-200]))
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
