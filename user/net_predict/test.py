# coding: utf-8
# @author  : lin
# @time    : 19-3-6

from user.net_predict.bp_train import bp_train
from user.net_predict.bp_predict import bp_predict
from db_model.model_dao import VegetablePriceModelDao, VegetableModelDao

all_model = VegetablePriceModelDao.query_vegetable_price_data()
price_list = [model.price for model in all_model]
# print(len(price_list))
# data = bp_train(price_list[:1070], '丝瓜')
# print(data)
data = bp_predict(price_list[:100], '丝瓜')
print(data)
print(len(price_list[:100]))
