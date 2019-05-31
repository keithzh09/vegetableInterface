# coding: utf-8
# @author  : lin
# @time    : 19-3-1

from playhouse.shortcuts import dict_to_model
from peewee import DoesNotExist
from traceback import format_exc


class DBFuncClass:
    @staticmethod
    def query_data(db_model, condition):
        """
        查询数据
        :param db_model: 数据库表model
        :param condition: 查询条件
        :return: 数据model
        """
        try:
            return db_model.select().where(condition).execute()
        except Exception as error:
            print(error)
            return False

    @staticmethod
    def insert_data(db_model, dict_data):
        """
        插入数据
        :param db_model: 数据库表model
        :param dict_data: 插入的数据
        :return: True or False
        """
        # 字典转为数据对象
        model = dict_to_model(db_model, dict_data)
        try:
            model.save()
            return True
        except Exception as error:
            print(error)
            return False

    @staticmethod
    def update(db_model, dict_data, condition):
        """
        更新
        :param db_model: 数据库表model
        :param dict_data: 更新的数据
        :param condition:
        :return: True or False
        """
        model = dict_to_model(db_model, dict_data)
        try:
            model.save().where(condition).execute()
            return True
        except Exception as error:
            print(error)
            return False

    @staticmethod
    def delete_data(db_model, condition):
        """
        删除数据
        :param db_model: 数据库表model
        :param condition: 条件
        :return: True or False
        """
        try:
            db_model.delete().where(condition).execute()
            return True
        except Exception as error:
            print(error)
            return False

    @staticmethod
    def get_one_obj(db_model, condition):
        """
        获取一条数据
        :return:
        """
        try:
            return db_model.get(condition)
        except DoesNotExist:
            return None
        except Exception as error:
            print(format_exc(error.__traceback__), type(error), error)
