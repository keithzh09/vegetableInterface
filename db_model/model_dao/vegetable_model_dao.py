# coding: utf-8
# @author  : lin
# @time    : 19-3-3

from ..model import VegetableModel
from peewee import DoesNotExist


class VegetableModelDao:
    @staticmethod
    def get_id_by_name(veg_name):
        try:
            obj = VegetableModel.get(VegetableModel.veg_name == veg_name)
            return obj.id
        except DoesNotExist:
            return None

    @staticmethod
    def get_information(veg_name):
        """
        通过蔬菜名查询数据
        :param veg_name:用户id
        :return:
        """
        try:
            obj = VegetableModel.get(VegetableModel.veg_name == veg_name)
            return obj.veg_information
        except DoesNotExist:
            return None

    @staticmethod
    def add_vegetable(veg_name, veg_information):
        """
        添加一种蔬菜的信息
        :param veg_name:
        :param veg_information:
        :return:
        """
        try:
            VegetableModel.insert(veg_name=veg_name, veg_information=veg_information).execute()
            return True
        except Exception as error:
            print(error)
            return False


