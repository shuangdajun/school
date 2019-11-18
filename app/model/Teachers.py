from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.model.Base import base, db

to_tea_sub=db.Table("to_tea_sub",
                    db.Column("id",Integer,primary_key=True,autoincrement=True),
                    db.Column("sub_id",Integer,ForeignKey("Subjects.subject_id")),
                    db.Column("tea_id",Integer,ForeignKey("Teachers.teacher_id"))
                    )
class Teachers(base):
    __tablename__="Teachers"
    teacher_id=Column(Integer,primary_key=True,autoincrement=True)
    teacher_name=Column(String(20),nullable=False,unique=True)
    teacher_address=Column(String(100))
    teacher_phone=Column(String(20))
    tea_sub=relationship("Subjects",secondary=to_tea_sub,backref="sub_tea",lazy="dynamic")
