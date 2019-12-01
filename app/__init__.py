import datetime
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
from app.model.Prices_warning import PricesWarn
from config.config import app_config
from flask_apscheduler import APScheduler
import re
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
db_connect=create_engine("mysql+pymysql://root:1qaz@WSX@172.18.1.101/fisher?charset=utf8",echo=True)
Session = sessionmaker(bind=db_connect)
session=Session()
def WarnPrices():
    # session.execute('select * from Prices where DATEDIFF("2019-11-27",stopTime)<=0')
    priwar=PricesWarn()
    pricesList=session.query(Prices).filter(db.cast(Prices.stopTime, db.Date) <= db.cast(datetime.date.today(), db.Date)).all()
    for price in pricesList:
        setattr(priwar,"student_name",price.pri_stu.student_name)
        if price.pri_tea!=None:
            setattr(priwar,"teacher_name",price.pri_tea.teacher_name)
        setattr(priwar,"subject_name",price.pri_sub.subject_name)
        setattr(priwar,"startTime",price.startTime)
        setattr(priwar,"stopTime",price.stopTime)
        setattr(priwar,"ClassHours",price.ClassHours)
        setattr(priwar,"prices",price.prices)
    result=session.query(PricesWarn).all()
    try:
        if len(result)!=0:
            session.execute("TRUNCATE table PricesWarn;")
        session.add(priwar)
        session.commit()
    except Exception as e:
        print(e)

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
Schuduler = APScheduler()  #定时任务
Schuduler.init_app(app)

api = Api(app=app, prefix="/api/v1")
from app import views
