# coding: utf-8
# @author  : lin
# @time    : 19-3-8

import json

from flask import request, Blueprint
from lib.http_response_code import response
from lib.decorator import catch_error
from .net_predict import bp_train, bp_predict, lstm_train, lstm_predict
from .dao import day_increase, day_decrease
from db_model.model_dao import UserModelDao, VegetableModelDao, VegetablePriceModelDao, PredictModelModelDao

model_app = Blueprint("model", __name__)


@model_app.route('information', methods=['POST'])
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


@model_app.route('predict', methods=['POST'])
@catch_error
def predict_price():
    """
    选择模型进行预测, 控制好id为1是指bp, id为2是指lstm
    :return:
    """
    req_json = request.json
    model_name = req_json['model_name']
    veg_name = req_json['veg_name']
    start_date = req_json['start_date']
    if not (model_name and veg_name and start_date):
        return json.dumps(response[20101], ensure_ascii=False)
    model_id = PredictModelModelDao.get_id_by_name(model_name)
    if model_id == -1:
        return json.dumps(response[20501], ensure_ascii=False)
    veg_id = VegetableModelDao.get_id_by_name(veg_name)
    pre_date = day_decrease(start_date, 150)[:10]
    veg_model_list = VegetablePriceModelDao.query_vegetable_price_data(2, veg_id, pre_date, start_date)
    price_list = [veg_model.price for veg_model in veg_model_list][-100:]  # 只取100个
    if model_id == 1:
        new_price_list = bp_predict(price_list, veg_name)
    elif model_id == 2:
        new_price_list = lstm_predict(price_list, veg_id, veg_name)
    else:
        # todo: ARIMA模型的数据获取，new_price_list为十个价格的数组
        new_price_list = None
    date_list = []
    the_date = start_date
    for i in range(10):
        the_date = day_increase(the_date, 1)[:10]
        date_list.append(the_date)
    response_data = {'date': date_list, 'predict_price': new_price_list}
    response_data.update(response[200])
    return json.dumps(response_data)


@model_app.route('network_train', methods=['POST'])
@catch_error
def network_train():
    """
    模型的训练
    :return:
    """
    req_json = request.json
    model_name = req_json['model_name']
    veg_name = req_json['veg_name']
    if not (model_name and veg_name):
        return json.dumps(response[20101], ensure_ascii=False)
    model_id = PredictModelModelDao.get_id_by_name(model_name)
    if model_id == -1:
        return json.dumps(response[20501], ensure_ascii=False)
    veg_id = VegetableModelDao.get_id_by_name(veg_name)
    veg_model_list = VegetablePriceModelDao.query_vegetable_price_data(1, veg_id)
    price_list = [veg_model.price for veg_model in veg_model_list][-1060:]
    if model_id == 1:
        response_data = bp_train(price_list, veg_name)
    else:
        response_data = lstm_train(price_list, veg_id, veg_name)
    response_data.update(response[200])
    return json.dumps(response_data)
