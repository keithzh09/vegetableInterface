# coding: utf-8
# @author  : lin
# @time    : 19-3-4
"""
建表和删除表
由于peewee的表封装成了类的形式，
因此可以通过传参进行传递，
便于写重复利用的function
"""


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

