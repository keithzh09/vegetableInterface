# coding: utf-8
# @author  : lin
# @time    : 19-3-3

from db_model.model import BaseModel
from peewee import CharField, BigIntegerField


class GroupModel(BaseModel):
    group_name = CharField()

    class Meta:
        db_table = 'group'
