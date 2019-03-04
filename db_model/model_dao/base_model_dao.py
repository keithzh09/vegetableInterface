# coding: utf-8
# @author  : lin
# @time    : 19-3-4
from ..model import UserModel, GroupModel, GroupPowerModel, PredictModelModel, VegetableModel, \
    VegetablePriceModel, VegetablePredictModelModel


def create_table(table):
    """
    如果table不存在，新建table
    """
    if not table.table_exists():
        table.create_table()


def drop_table(table):
    """
    table 存在，就删除
    """
    if table.table_exists():
        table.drop_table()


def create_all_table():
    create_table(UserModel)
    create_table(GroupModel)
    create_table(GroupPowerModel)
    create_table(PredictModelModel)
    create_table(VegetableModel)
    create_table(VegetablePriceModel)
    create_table(VegetablePredictModelModel)


def drop_all_table():
    drop_table(UserModel)
    drop_table(GroupModel)
    drop_table(GroupPowerModel)
    drop_table(PredictModelModel)
    drop_table(VegetableModel)
    drop_table(VegetablePriceModel)
    drop_table(VegetablePredictModelModel)

