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
            return user_obj.id if user_obj.user_pwd == user_pwd else -2

    @staticmethod
    def find_by_user_id(user_id):
        """
        通过用户ID查询数据
        :param user_id:用户id
        :return:
        """
        try:
            return UserModel.get(UserModel.id == user_id)
        except DoesNotExist:
            return None

    @staticmethod
    def add_user(user_name, user_pwd, email):
        """
        创建新用户，user_state在数据库设置默认值为1
        :param user_name: 用户名
        :param user_pwd: 用户密码
        :param email: 邮箱
        :return:
        """
        try:
            user_pwd = md5_encrypt(user_pwd)
            UserModel.insert(user_name=user_name, user_pwd=user_pwd, email=email).execute()
            return True
        except Exception as error:
            print(error)
            return False

    @staticmethod
    def query_user(func_code, user_name="", email="", group_id=1, user_state=-1):
        """
        查找用户
        :param func_code: 条件类型，0为查找某个状态的，1为按用户名查找和状态查找，2为按用户邮箱和状态查找，3为按
        用户组查找
        :param group_id: 用户组
        :param user_name: 用户名
        :param email: 邮箱
        :param user_state: 用户状态
        :return: model列表
        """
        try:
            if user_state == 0 or user_state == 1:
                if func_code:
                    if func_code == 1:
                        func = UserModel.select().where((UserModel.user_state == user_state) &
                                                        (UserModel.user_name == user_name))
                    elif func_code == 2:
                        func = UserModel.select().where((UserModel.user_state == user_state) &
                                                        (UserModel.email == email))
                    else:
                        func = UserModel.select().where((UserModel.user_state == user_state) &
                                                        (UserModel.group_id == group_id))
                else:
                    func = UserModel.select().where(UserModel.user_state == user_state)
            else:
                if func_code:
                    if func_code == 1:
                        func = UserModel.select().where(UserModel.user_name == user_name)
                    elif func_code == 2:
                        func = UserModel.select().where(UserModel.email == email)
                    else:
                        func = UserModel.select().where(UserModel.group_id == group_id)
                else:
                    func = UserModel.select().where(UserModel.id > 0)
            return func.execute()
        except Exception as error:
            print(error)
            return False

    @staticmethod
    def set_user_state(user_name, user_state):
        """
        设置用户状态
        :param user_name: 用户ID
        :param user_state: 用户状态，1为启动，0为禁止
        :return:
        """
        try:
            UserModel.update(user_state=user_state).where(UserModel.user_name == user_name).execute()
            return True
        except Exception as error:
            print(error)
            return False

    @staticmethod
    def alter_user_pwd(user_name, user_pwd):
        """
        修改用户密码
        :param user_name: 用户名
        :return:
        """
        try:
            user_pwd = md5_encrypt(user_pwd)
            UserModel.update(user_pwd=user_pwd).where(UserModel.user_name == user_name).execute()
        except Exception as error:
            print(error)
            return False

    @staticmethod
    def set_group_id(user_name, group_id):
        """
        设置用户组id，即添加或删除管理员
        :param user_name: 用户名
        :param group_id: 用户组id，2为管理员，1为普通用户
        :return:
        """
        try:
            UserModel.update(group_id=group_id).where(UserModel.user_name == user_name).execute()
            return True
        except Exception as error:
            print(error)
            return False

    @staticmethod
    def get_ui_config():
        columns = [
            {'title': '用户名', 'key': 'user_name', 'align': 'center'},
            {'title': '用户密码', 'key': 'user_pwd', 'align': 'center'},
            {'title': '用户状态', 'key': 'user_state', 'align': 'center'},
            {'title': '用户邮箱', 'key': 'email', 'align': 'center'},
        ]
        return columns
