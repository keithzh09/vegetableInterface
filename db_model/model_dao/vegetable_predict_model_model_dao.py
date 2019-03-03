# coding: utf-8
# @author  : lin
# @time    : 19-3-3
from ..model import VegetablePredictModelModel
from peewee import DoesNotExist


class VegetablePredictModelModelDao:
    @staticmethod
    def get_save_url(veg_id, model_id):
        """
        通过蔬菜id和模型id查询数据
        :param veg_id:
        :param model_id:
        :return:
        """
        try:
            # get方式仅返回一条数据
            obj = VegetablePredictModelModel.get((VegetablePredictModelModel.veg_id == veg_id) &
                                                 (VegetablePredictModelModel.model_id == model_id))
            return obj.url
        except DoesNotExist:
            return None

    @staticmethod
    def alter_save_url(veg_id, model_id, save_url):
        """
        修改模型存放路径
        :param veg_id:
        :param model_id:
        :param save_url:
        :return:
        """
        try:
            VegetablePredictModelModel.update(save_url=save_url).where((VegetablePredictModelModel.veg_id == veg_id) &
                                                                       (VegetablePredictModelModel.model_id == model_id)
                                                                       )
            return True
        except Exception as error:
            print(error)
            return False
