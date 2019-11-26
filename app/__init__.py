import os

from flask import Flask
from flask_login import LoginManager
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from app.model.Base import db


from app.model.Students import Students
from app.model.Subjects import Subjects
from app.model.Teachers import Teachers
from app.model.Prices import Prices

from config.config import app_config

import re

def accept_pattern(content,pattern_str):
    return re.match(pattern_str,content).group(1)


#db = SQLAlchemy()

login_manager = LoginManager()


def create_app(configuration):
    app = Flask(__name__)
    app.config.from_object(app_config[configuration])

    env=app.jinja_env
    env.filters["accept_pattern"]=accept_pattern  #定义jinja模板
    db.init_app(app)
    #创建所有表
    db.create_all(app=app)

    login_manager.init_app(app)
    login_manager.login_view = "login"

    return app


app = create_app(os.getenv('ENVIRONMENT'))
api = Api(app=app, prefix="/api/v1")
from app import views
#app.run(host="172.18.24.17",port="5000",debug=