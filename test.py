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
# VegetableModelDao.add_vegetable('白萝卜', '嘿哟嘿哟拔萝卜')
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

# UserModelDao.add_user('lin', '111222', '903784307@qq.com')
#
# for i in range(20):
#     user_name = 'user'+str(i)
#     UserModelDao.add_user(user_name, '111111', '903784307@qq.com')
#
# for i in range(20):
#     user_name = 'manager'+str(i)
#     UserModelDao.add_user(user_name, '111111', '903784307@qq.com')
# #
# sss = 'http://127.0.0.1:8080/root/login'
# print(sss.split('/'))
#
# GroupPowerModelDao.add_one_power(3, '/root/get_user_data')
# GroupPowerModelDao.add_one_power(3, '/root/get_user_ui')
# GroupPowerModelDao.add_one_power(3, '/root/add_manager')
# GroupPowerModelDao.add_one_power(3, '/root/delete_manager')
# GroupPowerModelDao.add_one_power(3, '/root/get_info')

# VegetableModelDao.add_vegetable('白萝卜', '它是白萝卜')
# VegetableModelDao.add_vegetable('茄瓜', '它是茄瓜')
# VegetableModelDao.add_vegetable('丝瓜', '它是丝瓜')


# print(VegetableModelDao.get_id_by_name('白萝卜'))
#
# # print(veg_data)
# print(VegetablePriceModelDao.delete_all_data())
#
#
# veg_data = pd.read_csv('白萝卜.csv').iloc[:, 0:4]
# isd = VegetableModelDao.get_id_by_name('白萝卜')
# print(isd)

# print(VegetablePriceModelDao.delete_all_data())
#
# start_t = time.time()
# isd = VegetableModelDao.get_id_by_name('白萝卜')
# for index, row in veg_data.iterrows():
#     VegetablePriceModelDao.add_one_data(isd, row['date'], row['price'], row['place'])
# stop_t = time.time()
#
# print(stop_t-start_t)

# start_t = time.time()
# isd = VegetableModelDao.get_id_by_name('白萝卜')
# all_data = []
# for index, row in veg_data.iterrows():
#     all_data.append((isd, row['date'], row['price'], row['place']))
# VegetablePriceModelDao.add_many_data(all_data)
# stop_t = time.time()
#
# print(stop_t-start_t)

#
# veg_data = pd.read_csv('茄瓜.csv').iloc[:, 0:4]
# # print(veg_data)
# # print(VegetablePriceModelDao.delete_all_data())
#
# start_t = time.time()
# isd = VegetableModelDao.get_id_by_name('茄瓜')
# for i in VegetablePriceModelDao.query_vegetable_price_data(1, isd):
#     print(i)
# for index, row in veg_data.iterrows():
#     VegetablePriceModelDao.add_one_data(isd, row['date'], row['price'], row['place'])
# stop_t = time.time()
# for i in VegetablePriceModelDao.query_vegetable_price_data(1, isd):
#     print(i)
# print(stop_t-start_t)


from db_model.model_dao import VegetableModelDao

# VegetableModelDao.alter_info('白菜', '它是白菜')
# VegetableModelDao.alter_url('白菜', '/usr/data/img.png')
# VegetableModelDao.add_vegetable('傻逼', '不死的白色不打算', 'user/sjda/sda')

# UserModelDao.alter_user_pwd('dibiao175', '123456')
# import os
#
#
# def file_name(file_dir):
#     for root, dirs, files in os.walk(file_dir):
#         data = []
#         print('[')
#         for i in files:
#             print('"', end='')
#             a = i.split('.')[0]
#             print(a+'",', end='')
#         print(']')
#
#
# start_t = time.time()
# for root, dirs, files in os.walk('network/veg_data_18_12/'):
#     print(root)
#     for file in files:
#         veg_name = file.split('.')[0]
#         veg_id = VegetableModelDao.get_id_by_name(veg_name)
#         uri = root + file
#         veg_data = pd.read_csv(uri)
#         VegetablePriceModelDao.add_many_data(veg_data)
# stop_t = time.time()
# print(stop_t-start_t)

# start_t = time.time()
# isd = VegetableModelDao.get_id_by_name('白萝卜')
# all_data = []
# for index, row in veg_data.iterrows():
#     all_data.append((isd, row['date'], row['price'], row['place']))
# VegetablePriceModelDao.add_many_data(all_data)
# stop_t = time.time()

# print(stop_t-start_t)

# from datetime import datetime, timedelta
# today_time = datetime.now()
# yes_day = today_time + timedelta(days=-1)
# today_time = today_time.strftime('%Y-%m-%d %H:%M:%s').split(' ')
# hour = today_time[1].split(':')[0]
# minute = today_time[1].split(':')[1]
# if int(hour) > 20 or (int(hour) == 20 and int(minute) >= 1):
#     print(yes_day.strftime('%Y-%m-%d %H:%M:%s'))
# print(hour)

# strs = '2019/02/10'
# strs = strs.replace('/', '-')
# print(strs)

import os
csv_save_path = 'csv_save_path/'
# 将蔬菜数据录入数据库
i = 1
start_t = time.time()
data = []
for root, dirs, files in os.walk(csv_save_path):
    for file in files:
        # print(i)
        veg_name = file.split('.')[0]
        veg_id = VegetableModelDao.get_id_by_name(veg_name)
        if veg_id is not None:
            i = i+1
            data.append(veg_name)
            uri = root + file
            # veg_data = pd.read_csv(uri)
            # VegetablePriceModelDao.add_many_data(veg_id, veg_data)
print(data)
print(len(data))
stop_t = time.time()
print(stop_t - start_t, 's')
data = ["葫芦瓜", "鲜冬菇", "云南小瓜", "芦笋", "西芹", "槟芋", "西兰花", "韭菜", "荷兰豆", "西生菜", "青瓜", "土豆",
        "椰菜花", "莴笋", "鲜淮山", "玉米", "韭菜花", "生菜", "青尖椒", "鲜百合", "莲藕", "园椒", "菠菜", "芫茜",
        "白豆角", "红葱头", "本地芹菜", "本地菜心", "葱", "韭黄", "鲜人参", "南瓜", "蒜心", "芥兰", "玉豆", "大蒜",
        "鲜虫草", "甜墨豆", "茄瓜", "苦瓜", "马蹄", "紫椰菜", "油麦菜", "红萝卜", "茶树菇", "西红柿", "大芋头", "矮脚白菜",
        "粉葛", "洋葱头", "金针菇", "百灵菇", "椰菜", "丝瓜", "红尖椒", "春菜", "蒜肉", "蒜头", "包心芥菜", "青皮冬瓜",
        "白萝卜", "小塘白菜", "沙姜", "大肉姜", "绍菜", "红薯", "节瓜", "日本豆腐", "沙葛", "娃娃菜"]