# coding: utf-8
# @author  : lin
# @time    : 19-3-3

from ..model import GroupModel
from peewee import DoesNotExist


class GroupModelDao:
    @staticmethod
    def find_by_group_id(group_id):
        """
        通过用户组ID查询数据，非空即存在
        :param group_id:用户id
        :return:
        """
        try:
            return GroupModel.get(GroupModel.group_id == group_id)
        except DoesNotExist:
            return None

    @staticmethod
    def add_group(group_name):
        """
        创建新用户组
        :param group_name: 用户组名
        :return:
        """
        try:
            GroupModel.insert(group_name=group_name).execute()
            return True
        except Exception as error:
            print(error)
            return False

    @staticmethod
    def query_group(func_code, group_name):
        """
        查找用户
        :param func_code: 条件类型，0为查找全部，1为按组名查找
        :param group_name: 用户组名
        :return: model列表
        """
        try:
            if func_code == 1:
                func = GroupModel.select().where(GroupModel.group_name == group_name)
            else:
                func = GroupModel.select().where(GroupModel.user_id > 1)
            return func.execute()
        except Exception as error:
            print(error)
            return False

