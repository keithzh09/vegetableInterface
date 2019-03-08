# coding: utf-8
# @author  : lin
# @time    : 19-3-6

from model_predict.net_predict import lstm_train, lstm_predict, bp_train, bp_predict
from db_model.model_dao import VegetablePriceModelDao

all_model = VegetablePriceModelDao.query_vegetable_price_data()
price_list = [model.price for model in all_model]
# print(len(price_list))
data = bp_train(price_list[:1060], '丝瓜')
# print(data)
# data = bp_predict(price_list[:100], "丝瓜")
# data = lstm_predict(price_list[:100], "1", '丝瓜')
# data = lstm_train(price_list[:1060], "1", '丝瓜')
print(data)
