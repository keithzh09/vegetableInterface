# coding: utf-8
# @author  : lin
# @time    : 19-3-3

from db_model.model import BaseModel
from peewee import CharField, IntegerField, BigIntegerField, DateTimeField, FloatField


class VegetablePriceModel(BaseModel):
    veg_id = BigIntegerField()
    date = CharField()
    price = FloatField()
    place = CharField()

    class Meta:
        db_table = 'vegetable_price'
