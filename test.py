# coding: utf-8
# @author  : lin
# @time    : 19-3-5

from db_model.model_dao import VegetablePriceModelDao, VegetableModelDao, PredictModelModelDao
from cron_spider import spider_vegetable
#
import pandas as pd
import time
# drop_all_table()
# create_all_table()

VegetableModelDao.add_vegetable('白菜', '它是一种白菜啊！！！')


print(VegetableModelDao.get_id_by_name('白菜'))

veg_data = pd.read_csv('丝瓜.csv').iloc[:, 1:4]
print(veg_data)
# print(VegetablePriceModelDao.delete_all_data())

start_t = time.time()
isd = VegetableModelDao.get_id_by_name('白菜')
for index, row in veg_data.iterrows():
    VegetablePriceModelDao.add_one_data(isd, row['date'], row['price'], '山东')
stop_t = time.time()

# print(stop_t-start_t)

# PredictModelModelDao.add_model('bp', 'is bp network!')
# PredictModelModelDao.add_model('lstm', 'is lstm network')

