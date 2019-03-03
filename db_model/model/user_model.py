# coding: utf-8
# @author  : lin
# @time    : 19-3-3

from db_model.model import BaseModel
from peewee import CharField, IntegerField, BigIntegerField, DateTimeField


class UserModel(BaseModel):
    user_id = BigIntegerField(primary_key=True)
    group_id = BigIntegerField()
    user_name = CharField()
    user_pwd = CharField()
    user_state = IntegerField()

    class Meta:
        db_table = 'user'
