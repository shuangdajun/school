from flask import request

from app import db
from app.model.Students import Students
from app.model.Subjects import Subjects
from app.model.Teachers import Teachers

def add_student_db(form_dict,subjectList):
    student = Students()
    for key, value in form_dict:
        if hasattr(student, key):
            setattr(student, key, value)
        elif key=="subjectSelect":
            value=Subjects.query.filter(Subjects.subject_name.in_(subjectList)).all()
            setattr(student, "stu_sub", value)
    try:
        db.session.add(student)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)


def delete_student_db(args):
    try:
        result=db.session.query(Students).filter_by(student_name=args["delete_student"]).first()

        for value in result.stu_pri:
            db.session.delete(value)
        db.session.delete(result)

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)


def editor_student_db(args,form):
    student_name = args["search"]
    student=Students.query.filter_by(student_name=student_name).first()
    subject_list=[]
    for subject in form.getlist("subjectSelect"):
        subject_list.append(Subjects.query.filter_by(subject_name=subject).first())

    try:
        student.student_name=form["student_name"]
        student.student_age=form["student_age"]
        student.student_sex=form["student_sex"]
        student.student_phone=form["student_phone"]
        student.student_landline=form["student_landline"]
        student.stu_sub = subject_list

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)

def search_student_db(args,params_dict):
    if params_dict["search_student"]=="":
        result = Students.query.all()
        pagination, user = paginate_html_db(Students)
        return pagination, user
    if Students.query.filter_by(student_name=args.get("search_student")).all()==[]:
        return None
    return paginate_html_db(Students)[0],Students.query.filter_by(student_name=args.get("search_student")).all()


def paginate_html_db(Object,num=14):
    page=request.args.get("page",1,type=int)

    pagination=Object.query.paginate(page,per_page=num,error_out=False)#per_page超出时,error_out=False返回[]
    users=pagination.items
    return pagination,users

def search_stduent(student_name):
    student=Students.query.filter_by(student_name=student_name).first()
    return student




