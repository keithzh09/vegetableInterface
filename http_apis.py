# coding: utf-8
# @author: lin
# @date: 18-7-22

from flask import Flask
from flask_cors import *

app = Flask(__name__)

from user import user_app
from manager import manager_app
from root import root_app
from model_predict import model_app

CORS(app, resources=r'/*')
app.config.from_pyfile('config/email_config.py')

# 注册蓝图
app.register_blueprint(user_app, url_prefix='/user')
app.register_blueprint(manager_app, url_prefix='/manager')
app.register_blueprint(root_app, url_prefix='/root')
app.register_blueprint(model_app, url_prefix='/model')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
    # 定时爬虫任务,另开一个进程运行
