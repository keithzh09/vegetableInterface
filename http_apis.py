# coding: utf-8
# @author: lin
# @date: 18-7-22

from flask import Flask
from user import user_app

app = Flask(__name__)
app.register_blueprint(user_app, url_prefix='/user/')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=12006, debug=True)

