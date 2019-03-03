# coding: utf-8
# @author  : lin
# @time    : 19-3-3

from ..model import GroupPowerModel


class GroupPowerModelDao:
    # 设置为类函数，是为了能够调用静态函数
    @classmethod
    def check_group_permission(cls, group_id, api_url):
        """
        检查用户组是否有权限访问URL
        :param group_id: 用户组ID
        :param api_url: 接口URL
        :return: True or False
        """
        url_list = cls.get_urls_from_group_id(group_id)
        for url in url_list:
            if api_url.find(url) == 0:
                return True
        return False

    @staticmethod
    def get_urls_from_group_id(group_id):
        """
        获取用户组权限url列表
        :param group_id: 用户组ID
        :return:
        """
        objs = GroupPowerModel.select().where(GroupPowerModel.group_id == group_id)
        return [obj.url for obj in objs]
