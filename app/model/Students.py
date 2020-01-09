from sqlalchemy import Column, Integer, String, Float, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

from app.model.Base import base, db

to_stu_sub=db.Table("to_stu_sub",
                    db.Column("id",Integer,primary_key=True,autoincrement=True),
                    db.Column("stu_id",Integer,ForeignKey("Students.student_id")),
                    db.Column("sub_id",Integer,ForeignKey("Subjects.subject_id"))
                    )
class Students(base):
    __tablename__ = "Students"
    student_id=Column(Integer,autoincrement=True,primary_key=True)
    student_name = Column(String(20),unique=True)
    student_sex=Column(String(10))
    student_age=Column(Integer)
    student_phone=Column(String(25))
    description=Column(String(100))
    stu_sub=db.relationship("Subjects",secondary=to_stu_sub,backref="sub_stu",lazy="dynamic")







#
# class Subjects(base):
#     __tablename__ = "Subjects"
#     subject_id=Column(Integer,autoincrement=True,primary_key=True)
#     subject_name=Column(String(50),nullable=False)
#     sub_pri = relationship("Prices", backref="pri_sub", lazy="dynamic")
#
#
# class Teachers(base):
#     __tablename__="Teachers"
#     teacher_id=Column(Integer,primary_key=True,autoincrement=True)
#     teacher_name=Column(String(20),nullable=False)
#     teacher_address=Column(String(100))
#     teacher_phone=Column(String(20))
#     tea_pri=relationship("Prices",backref="pri_tea",lazy="dynamic")
#
#
#
# class Prices(base):
#     __tablename__ = "Prices"
#     price_id=Column(Integer,primary_key=True,autoincrement=True)
#     stu_id=Column(Integer,ForeignKey("Students.student_id"))
#     sub_id = Column(Integer,ForeignKey("Subjects.subject_id"))
#     tea_id = Column(Integer,ForeignKey("Teachers.teacher_id"))
#     during_learning=Column(String(20))
#     arreas=Column(Float)
