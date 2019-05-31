# coding: utf-8
# @author  : lin
# @time    : 19-3-5

from db_model.model_dao import VegetablePriceModelDao, VegetableModelDao, PredictModelModelDao,\
    create_all_table, drop_all_table, UserModelDao, GroupPowerModelDao
from cron_spider import spider_vegetable

from db_model.model_dao import VegetablePriceModelDao, VegetableModelDao, drop_all_table, create_all_table
import pandas as pd
import time
# drop_all_table()
# create_all_table()

#
# import pandas as pd
# import time
# drop_all_table()
# create_all_table()
#
# VegetableModelDao.add_vegetable('白菜', '它是一种白菜啊！！！')
# PredictModelModelDao.add_model('bp', 'it\'s bp yes\nfuck you.')
#
# print(VegetableModelDao.get_id_by_name('白菜'))
#
# veg_data = pd.read_csv('丝瓜.csv').iloc[:, 1:4]
# print(veg_data)
# # print(VegetablePriceModelDao.delete_all_data())
#
# start_t = time.time()
# isd = VegetableModelDao.get_id_by_name('白菜')
# for index, row in veg_data.iterrows():
#     VegetablePriceModelDao.add_one_data(isd, row['date'], row['price'], '山东')
# stop_t = time.time()

# print(stop_t-start_t)

# PredictModelModelDao.add_model('bp', 'is bp network!')
# PredictModelModelDao.add_model('lstm', 'is lstm network')

# for i in range(20):
#     user_name = 'user'+str(i)
#     UserModelDao.add_user(user_name, '111111', '903784307@qq.com')
#
# for i in range(20):
#     user_name = 'manager'+str(i)
#     UserModelDao.add_user(user_name, '111111', '903784307@qq.com')
#
# sss = 'http://127.0.0.1:8080/root/login'
# print(sss.split('/'))

# GroupPowerModelDao.add_one_power(3, '/root/get_user_data')
# GroupPowerModelDao.add_one_power(3, '/root/get_user_ui')
# GroupPowerModelDao.add_one_power(3, '/root/add_manager')
# GroupPowerModelDao.add_one_power(3, '/root/delete_manager')
# GroupPowerModelDao.add_one_power(3, '/root/get_info')

# VegetableModelDao.add_vegetable('白萝卜', '它是白萝卜')
# VegetableModelDao.add_vegetable('茄瓜', '它是茄瓜')
# VegetableModelDao.add_vegetable('丝瓜', '它是丝瓜')


print(VegetableModelDao.get_id_by_name('白萝卜'))

# print(veg_data)
# print(VegetablePriceModelDao.delete_all_data())


veg_data = pd.read_csv('白萝卜.csv').iloc[:, 0:4]
# print(veg_data)
# print(VegetablePriceModelDao.delete_all_data())

start_t = time.time()
isd = VegetableModelDao.get_id_by_name('白萝卜')
for index, row in veg_data.iterrows():
    VegetablePriceModelDao.add_one_data(isd, row['date'], row['price'], row['place'])
stop_t = time.time()

print(stop_t-start_t)

veg_data = pd.read_csv('茄瓜.csv').iloc[:, 0:4]
# print(veg_data)
# print(VegetablePriceModelDao.delete_all_data())

start_t = time.time()
isd = VegetableModelDao.get_id_by_name('茄瓜')
for i in VegetablePriceModelDao.query_vegetable_price_data(1, isd):
    print(i)
for index, row in veg_data.iterrows():
    VegetablePriceModelDao.add_one_data(isd, row['date'], row['price'], row['place'])
stop_t = time.time()
for i in VegetablePriceModelDao.query_vegetable_price_data(1, isd):
    print(i)
print(stop_t-start_t)