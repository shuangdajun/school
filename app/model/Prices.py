import datetime

from sqlalchemy.orm import relationship

from app.model.Base import base, db
from sqlalchemy import Column,Integer,String,Float,ForeignKey,Date
from flask_sqlalchemy import SQLAlchemy
class Prices(base):
    __tablename__ = "Prices"
    price_id=Column(Integer,primary_key=True,autoincrement=True)
    stu_id=Column(Integer,ForeignKey("Students.student_id"),unique=True)

    tea_id = Column(Integer,ForeignKey("Teachers.teacher_id"))
    sub_id = Column(Integer, ForeignKey("Subjects.subject_id"))
    startTime=Column(Date,default=datetime.date.today())
    stopTime=Column(Date)
    ClassHours=Column(String(20))
    prices=Column(String(20))
    pri_stu=db.relationship("Students",backref="stu_pri")
    pri_tea = db.relationship("Teachers", backref="tea_pri")
    pri_sub = db.relationship("Subjects", backref="sub_pri")

