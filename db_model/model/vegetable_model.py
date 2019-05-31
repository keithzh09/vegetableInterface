# coding: utf-8
# @author  : lin
# @time    : 19-3-3

from db_model.model import BaseModel
from peewee import CharField, BigIntegerField, TextField


class VegetableModel(BaseModel):
    veg_name = CharField()
    veg_information = TextField()

    class Meta:
        db_table = 'vegetable'
