# coding: utf-8
# @author  : lin
# @time    : 19-3-3

from peewee import Model, MySQLDatabase
from config import db_config


mysql_config = db_config.mysql_config
db = MySQLDatabase(mysql_config['db_name'], user=mysql_config['db_user'], password=mysql_config['db_password'],
                   host=mysql_config['db_host'], port=mysql_config['db_port'])


class BaseModel(Model):
    class Meta:
        database = db
