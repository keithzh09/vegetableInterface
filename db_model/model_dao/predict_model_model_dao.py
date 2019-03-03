# coding: utf-8
# @author  : lin
# @time    : 19-3-3

from ..model import PredictModelModel
from peewee import DoesNotExist


class PredictModelModelDao:
    @staticmethod
    def get_information(model_name):
        """
        通过模型名查询数据
        :param model_name:模型名
        :return:
        """
        try:
            obj = PredictModelModel.get(PredictModelModel.model_name == model_name)
            return obj.veg_information
        except DoesNotExist:
            return None

    @staticmethod
    def add_model(model_name, model_information):
        """
        添加一种模型的信息
        :param model_name:
        :param model_information:
        :return:
        """
        try:
            PredictModelModel.insert(model_name=model_name, model_information=model_information).execute()
            return True
        except Exception as error:
            print(error)
            return False
