# coding: utf-8
# @author  : lin
# @time    : 19-3-3

from db_model.model import BaseModel
from peewee import CharField, BigIntegerField


class VegetablePredictModelModel(BaseModel):
    veg_id = BigIntegerField()
    model_id = BigIntegerField()
    save_url = CharField()  # 模型存放路径

    class Meta:
        db_table = 'vegetable_predict_model'
