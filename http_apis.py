# coding: utf-8
# @author: lin
# @date: 18-7-22

from flask import Flask
from user import user_app
from db_model import model_dao

app = Flask(__name__)
app.config.from_pyfile('config/email_config.py')
app.register_blueprint(user_app, url_prefix='/user/')


if __name__ == '__main__':
    model_dao.create_all_table()
    app.run(host='127.0.0.1', port=12006, debug=True)


