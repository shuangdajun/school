from sqlalchemy import Column,Integer,String,Float
from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()
class base(db.Model):
    __abstract__=True #子类引用基类时不会创建基类表
    # student_name=Column(String(20))



# conn_stu_sub=db.Table(
#     "Stu_Sub",
#     db.Column("id",Integer,primary_key=True,autoincrement=True),
#     db.Column("stu_name",db.Integer,db.ForeignKey("Students.student_id")),
#     db.Column("sub_name",db.Integer,db.ForeignKey("Subjects.subject_id"))
# )