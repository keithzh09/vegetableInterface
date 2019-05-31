# coding: utf-8
# @author  : lin
# @time    : 19-3-3

from db_model.model import BaseModel
from peewee import CharField, BigIntegerField, TextField


class PredictModelModel(BaseModel):
    model_name = CharField()
    model_information = TextField()

    class Meta:
        db_table = 'predict_model'
