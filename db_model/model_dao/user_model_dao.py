# coding: utf-8
# @author  : lin
# @time    : 19-3-3

from ..model import UserModel
from peewee import DoesNotExist
from lib.MD5_encrypt import md5_encrypt


class UserModelDao:
    @staticmethod
    def check_user_and_user_pwd(user_name, user_pwd):
        """
        检查user_code和user_key
        :param user_name: 用户名
        :param user_pwd: 用户密码
        :return: 验证通过：user_id， 不存在用户：-1，密码错误：-2
        """
        try:
            user_obj = UserModel.get(UserModel.user_name == user_name)
        except DoesNotExist:
            return -1
        else:
            # 将user_key先MD5加密
            user_pwd = md5_encrypt(user_pwd)
            return user_obj.user_id if user_obj.user_pwd == user_pwd else -2

    @staticmethod
    def find_by_user_name(user_name):
        """
        通过用户ID查询数据
        :param user_name:用户名
        :return:
        """
        try:
            return UserModel.get(UserModel.user_name == user_name)
        except DoesNotExist:
            return None

    @staticmethod
    def add_user(user_name, user_pwd, group_id):
        """
        创建新用户，user_state在数据库设置默认值为1
        :param user_name: 用户名
        :param user_pwd: 用户密码
        :param group_id: 用户组ID
        :return:
        """
        try:
            user_pwd = md5_encrypt(user_pwd)
            UserModel.insert(user_name=user_name, user_pwd=user_pwd, group_id=group_id).execute()
            return True
        except Exception as error:
            print(error)
            return False

    @staticmethod
    def query_user(func_code, user_name="", user_state=1):
        """
        查找用户
        :param func_code: 条件类型，0为查找全部，1为按用户名查找，2为按用户状态查找，3为按组合条件查找
        :param user_name: 用户名
        :param user_state: 用户状态
        :return: model列表
        """
        try:
            if func_code:
                if func_code == 1:
                    func = UserModel.select().where(UserModel.user_name == user_name)
                elif func_code == 2:
                    func = UserModel.select().where(UserModel.user_state == user_state)
                else:
                    func = UserModel.select().where((UserModel.user_name == user_name) &
                                                    (UserModel.user_state == user_state))
            else:
                func = UserModel.select().where(UserModel.user_id > 1)
            return func.execute()
        except Exception as error:
            print(error)
            return False

    @staticmethod
    def set_user_state(user_id, user_state):
        """
        设置用户状态，不显式删除，禁用即可
        :param user_id: 用户ID
        :param user_state: 用户状态，1为启动，0为禁止
        :return:
        """
        try:
            UserModel.update(user_state=user_state).where(UserModel.user_id == user_id).execute()
            return True
        except DoesNotExist:
            return False
