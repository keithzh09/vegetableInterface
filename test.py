# coding: utf-8
# @author  : lin
# @time    : 19-3-5

import pandas as pd
from db_model.model_dao import VegetableModelDao, VegetablePriceModelDao
import time

# VegetableModelDao.add_vegetable('矮脚白菜', '它是一种白菜啊！！！')

print(VegetableModelDao.get_id_by_name('矮脚白菜'))

baicai_data = pd.read_csv('baicai.csv').iloc[:, 0:3]
print(VegetablePriceModelDao.delete_all_data())

start_t = time.time()
isd = VegetableModelDao.get_id_by_name('矮脚白菜')
for index, row in baicai_data.iterrows():
    VegetablePriceModelDao.add_one_data(isd, row['date'], row['price'], '山东')
stop_t = time.time()

print(stop_t-start_t)
