from sqlalchemy.orm import relationship

from app.model.Base import base, db
from sqlalchemy import Column,Integer,String,Float,ForeignKey
from flask_sqlalchemy import SQLAlchemy


class Subjects(base):
    __tablename__ = "Subjects"
    subject_id=Column(Integer,autoincrement=True,primary_key=True)
    # teacher_id=Column(Integer,ForeignKey("Teachers.teacher_id"))
    # student_id=Column(Integer,ForeignKey("Students.student_id"))
    subject_name=Column(String(50))
    class_name=Column(String(50))
    description=Column(String(100))


    # sub_to_stu=db.relationship("Students",secondary=conn_stu_sub,backref="stu_to_sub",lazy="dynamic") #secondary表示中间关联的表


