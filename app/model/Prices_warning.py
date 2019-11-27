import datetime

from sqlalchemy import Column,String,Integer,Date

from app.model.Base import base


class PricesWarn(base):
    __tablename__="PricesWarn"
    price_id=Column(Integer,primary_key=True,autoincrement=True)
    student_name=Column(String(20))
    teacher_name=Column(String(20))
    subject_name=Column(String(20))
    startTime=Column(Date,default=datetime.date.today())
    stopTime=Column(Date)
    ClassHours=Column(String(20))
    prices=Column(String(20))

