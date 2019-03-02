# coding: utf-8
# @author  : lin
# @time    : 19-3-3

from db_model.model import BaseModel
from peewee import CharField, BigIntegerField


class VegetableModel(BaseModel):
    veg_id = BigIntegerField(primary_key=True)
    veg_name = CharField()
    veg_information = CharField()

    class Meta:
        db_table = 'vegetable'
