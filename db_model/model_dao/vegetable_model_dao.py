# coding: utf-8
# @author  : lin
# @time    : 19-3-3

from ..model import VegetableModel
from peewee import DoesNotExist, chunked


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
    def add_vegetable(veg_name, veg_information, veg_img_url=''):
        """
        添加一种蔬菜的信息
        :param veg_name:
        :param veg_information:
        :param veg_img_url: 图片路径
        :return:
        """
        try:
            VegetableModel.insert(veg_name=veg_name, veg_information=veg_information, veg_img_url=veg_img_url).execute()
            return True
        except Exception as error:
            print(error)
            return False

    @staticmethod
    def add_many_data(all_data):
        """
        同时插入很多数据
        all_data的格式要符合field，ed. [('地瓜', '是地瓜', '/sda/sdas/ssd.img'), (...)]，本质是list&tuple
        :return:
        """
        try:
            field = [VegetableModel.veg_name, VegetableModel.veg_information,
                     VegetableModel.place]
            for data_chunk in chunked(all_data, 1000):
                VegetableModel.insert_many(data_chunk, field).execute()
        except Exception as error:
            print(error)
            return False

    @staticmethod
    def alter_info(veg_name, veg_information):
        """
        修改描述
        :return:
        """
        try:
            VegetableModel.update(veg_information=veg_information).where(VegetableModel.veg_name == veg_name).execute()
            return True
        except Exception as error:
            print(error)
            return False

    @staticmethod
    def alter_url(veg_name, veg_img_url):
        """
        修改图片路径
        :return:
        """
        try:
            VegetableModel.update(veg_img_url=veg_img_url).where(VegetableModel.veg_name == veg_name).execute()
            return True
        except Exception as error:
            print(error)
            return False

    @staticmethod
    def delete_vegetable(veg_name):
        """
        删除蔬菜信息
        :param veg_name:
        :return:
        """
        try:
            VegetableModel.delete().where(VegetableModel.veg_name == veg_name).execute()
            return True
        except Exception as error:
            print(error)
            return False

    @staticmethod
    def query_vegetable():
        """
        查找所有蔬菜
        """
        try:
            func = VegetableModel.select().where(VegetableModel.id > 0)
            return func.execute()
        except Exception as error:
            print(error)
            return False

