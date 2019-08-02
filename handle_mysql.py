# coding: utf-8
# @author  : lin
# @time    : 2019/8/2
from db_model.model_dao import VegetablePriceModelDao, VegetableModelDao, PredictModelModelDao,\
    create_all_table, drop_all_table, UserModelDao, GroupPowerModelDao, GroupModelDao
from cron_spider import spider_vegetable

from db_model.model_dao import VegetablePriceModelDao, VegetableModelDao, drop_all_table, create_all_table
import pandas as pd
import time

UserModelDao.add_user('SuperVisitor', 'veg_root#2019', 'veg_root@test.com')
UserModelDao.set_group_id('SuperVisitor', 3)

GroupModelDao.add_group('普通用户')
GroupModelDao.add_group('管理员')
GroupModelDao.add_group('超级管理员')

PredictModelModelDao.add_model('bp', 'bp神经网络')
PredictModelModelDao.add_model('lstm', 'lstm神经网络')
PredictModelModelDao.add_model('arima', 'arima时间序列')

GroupPowerModelDao.add_one_power(3, '/root/get_user_data')
GroupPowerModelDao.add_one_power(3, '/root/get_user_ui')
GroupPowerModelDao.add_one_power(3, '/root/add_manager')
GroupPowerModelDao.add_one_power(3, '/root/delete_manager')
GroupPowerModelDao.add_one_power(3, '/root/get_info')

GroupPowerModelDao.add_one_power(2, '/root/get_user_data')
GroupPowerModelDao.add_one_power(2, '/root/get_user_ui')
GroupPowerModelDao.add_one_power(2, '/root/get_info')
