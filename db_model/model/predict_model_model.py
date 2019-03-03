# coding: utf-8
# @author  : lin
# @time    : 19-3-3

from db_model.model import BaseModel
from peewee import CharField, BigIntegerField


class PredictModelModel(BaseModel):
    model_id = BigIntegerField(primary_key=True)
    model_name = CharField()
    model_information = CharField()

    class Meta:
        db_table = 'predict_model'
