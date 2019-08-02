# coding: utf-8
# @author: lin
# @date: 18-7-22

from flask import Flask
from flask_cors import *
from multiprocessing import Process
from cron_spider import cron_task
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
    p = Process(target=cron_task, args=('20:00',))
    p.start()

    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='127.0.0.1', port=8080, debug=True)
    # 定时爬虫任务,另开一个进程运行
