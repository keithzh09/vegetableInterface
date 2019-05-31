# coding: utf-8
# @author  : lin
# @time    : 19-3-3

from ..model import GroupModel


class GroupModelDao:

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
        查找用户组
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

