# coding: utf-8
# @author  : lin
# @time    : 19-3-8

import json

from flask import request, Blueprint
from lib.http_response_code import response
from lib.decorator import catch_error
from .net_predict import bp_train, bp_predict, lstm_train, lstm_predict, bp_get_accuracy, lstm_get_accuracy
from .dao import day_increase, day_decrease
from db_model.model_dao import UserModelDao, VegetableModelDao, VegetablePriceModelDao, PredictModelModelDao
# import multiprocessing
from multiprocessing import Pool, Manager

pool = Pool(processes=4)
manager = Manager()
model_app = Blueprint("model", __name__)


@model_app.route('information', methods=['POST'])
@catch_error
def model_info():
    """
    获取模型信息
    :return:
    """
    model_name = request.json['model_name']
    if model_name:
        if PredictModelModelDao.get_id_by_name(model_name):
            model_information = PredictModelModelDao.get_information(model_name)
            if model_information is None:
                # 无模型信息
                response_data = response[20502]
            else:
                # 获取信息成功
                response_data = {'model_info': model_information}
                response_data.update(response[200])
        else:
            # 缺少模型
            response_data = response[20501]
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
    new_pool = Pool(processes=4)
    req_json = request.json
    model_name = req_json['model_name']
    veg_name = req_json['vegetable_name']
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
        # new_price_list = bp_predict(price_list, veg_name)
        # 以这个解决本地训练然后传到服务器进行测试的网络模型
        result = new_pool.apply_async(bp_predict, (price_list, veg_name,))
        new_price_list = result.get()
    elif model_id == 2:
        # new_price_list = lstm_predict(price_list, veg_id, veg_name)
        # 另开一个进程解决  <class 'ValueError'> Variable 1/rnn/basic_lstm_cell/kernel already exists, disallowed.
        result = new_pool.apply_async(lstm_predict, (price_list, veg_name,))
        new_price_list = result.get()
    else:
        # todo: ARIMA模型的数据获取，new_price_list为十个价格的数组
        new_price_list = None
    date_list = []
    the_date = start_date
    for i in range(10):
        the_date = day_increase(the_date, 1)[:10]
        date_list.append(the_date)
    data = {'date': date_list, 'predict_price': new_price_list}
    response_data = {'data': data}
    response_data.update(response[200])
    new_pool.close()
    new_pool.join()
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
    veg_list = req_json['vegetable_list']
    if not (model_name and veg_list):
        return json.dumps(response[20101], ensure_ascii=False)
    model_id = PredictModelModelDao.get_id_by_name(model_name)
    if model_id == -1:
        return json.dumps(response[20501], ensure_ascii=False)
    for veg_name in veg_list:
        veg_id = VegetableModelDao.get_id_by_name(veg_name)
        veg_model_list = VegetablePriceModelDao.query_vegetable_price_data(1, veg_id)
        price_list = [veg_model.price for veg_model in veg_model_list][-1060:]

        if model_id == 1:
            # 异步加入进程池
            pool.apply_async(bp_train, (price_list, veg_name,))
        else:
            pool.apply_async(lstm_train, (price_list, veg_id, veg_name,))
    return json.dumps(response[200])


@model_app.route('get_accuracy', methods=['POST'])
@catch_error
def get_accuracy():
    """
    模型的训练
    :return:
    """
    new_pool = Pool(processes=4)
    req_json = request.json
    model_name = req_json['model_name']
    veg_name = req_json['vegetable_name']
    if not (model_name and veg_name):
        return json.dumps(response[20101], ensure_ascii=False)
    model_id = PredictModelModelDao.get_id_by_name(model_name)
    if model_id == -1:
        return json.dumps(response[20501], ensure_ascii=False)
    veg_id = VegetableModelDao.get_id_by_name(veg_name)
    veg_model_list = VegetablePriceModelDao.query_vegetable_price_data(1, veg_id)
    price_list = [veg_model.price for veg_model in veg_model_list][-1060:]

    if model_id == 1:
        # response_data = bp_get_accuracy(price_list, veg_name)
        price_list = manager.list(price_list)
        result = new_pool.apply_async(bp_get_accuracy, (price_list, veg_name,))
        response_data = result.get()
    else:
        # response_data = lstm_get_accuracy(price_list, veg_id, veg_name)
        # 另开一个进程解决  <class 'ValueError'> Variable 1/rnn/basic_lstm_cell/kernel already exists, disallowed.
        price_list = manager.list(price_list)
        result = new_pool.apply_async(lstm_get_accuracy, (price_list, veg_id, veg_name,))
        response_data = result.get()
        # response_data = {}
    response_data.update(response[200])
    new_pool.close()
    new_pool.join()
    return json.dumps(response_data)
