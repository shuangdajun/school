import datetime
import os

from flask import Flask

from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from  flask_login import LoginManager
from app.model.Base import db #db只是在views中生效


from app.model.Students import Students
from app.model.Subjects import Subjects
from app.model.Teachers import Teachers
from app.model.Permission import Permission
from app.model.Role import Role
from app.model.Prices import Prices
from app.model.Prices_warning import PricesWarn
from app.model.User import User
from config.config import app_config
from flask_apscheduler import APScheduler
import re
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
db_connect=create_engine("mysql+pymysql://root:1qaz@WSX@172.18.1.101/fisher?charset=utf8",echo=True)
Session = sessionmaker(bind=db_connect)
session=Session()
def WarnPriceAtrr(pricesList):

    prilist=[]
    for price in pricesList:
        priwar = PricesWarn()
        setattr(priwar,"student_name",price.pri_stu.student_name)
        if price.pri_tea!=None:
            setattr(priwar,"teacher_name",price.pri_tea.teacher_name)
        setattr(priwar,"subject_name",price.pri_sub.subject_name)
        setattr(priwar,"startTime",price.startTime)
        setattr(priwar,"stopTime",price.stopTime)
        setattr(priwar,"ClassHours",price.ClassHours)
        setattr(priwar,"prices",price.prices)
        prilist.append(priwar)
    return prilist
def WarnPrices():
    # session.execute('select * from Prices where DATEDIFF("2019-11-27",stopTime)<=0')

    #cast函数可以将时间转换成日期
    pricesList=session.query(Prices).order_by(Prices.stopTime).filter(db.cast(Prices.stopTime, db.Date) <= db.cast(datetime.date.today()-datetime.timedelta(days=7), db.Date)).all()
    if pricesList==[]:
        return
    result=session.query(PricesWarn).all()
    try:
        if len(result)!=0:
            session.execute("TRUNCATE table PricesWarn;")
        session.add_all(WarnPriceAtrr(pricesList))
        session.commit()
    except Exception as e:
        print(e)

def accept_pattern(content,pattern_str):
    return re.match(pattern_str,content).group(1)


def create_app(configuration):
    # static_url_path表示前端必须就这个前缀开头才能访问static
    #static_folder表示后端static的工作目录
    app = Flask(__name__,static_folder="static/school_static",static_url_path="")

    app.config.from_object(app_config[configuration])

    env=app.jinja_env
    env.filters["accept_pattern"]=accept_pattern  #定义jinja模板
    db.init_app(app)
    #创建所有表
    db.create_all(app=app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view="login"
    #配置self.user_callback()回调函数，绑定user到当前请求上下文
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    return app




app = create_app(os.getenv('ENVIRONMENT'))
Schuduler = APScheduler()  #定时任务
Schuduler.init_app(app)

# api = Api(app=app, prefix="/api/v1")
from app import views
