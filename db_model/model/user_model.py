# coding: utf-8
# @author  : lin
# @time    : 19-3-3

from db_model.model import BaseModel
from peewee import CharField, IntegerField, BigIntegerField, DateTimeField


class UserModel(BaseModel):
    # 会自动创建id变量
    group_id = BigIntegerField(default=1)
    user_name = CharField(max_length=20)
    user_pwd = CharField(max_length=32)
    # 用户状态，默认为1（启用）
    user_state = IntegerField(default=1)
    email = CharField(max_length=30)

    class Meta:
        db_table = 'user'
