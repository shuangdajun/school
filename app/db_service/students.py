from flask import request

from app import db
from app.model.Students import Students
from app.model.Subjects import Subjects
from app.model.Teachers import Teachers
from app.service.detail_students import dict_if


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
        if subject:
            subject_name,class_name=subject.split("-")
        subject_list.append(Subjects.query.filter(Subjects.subject_name==subject_name, Subjects.class_name==class_name).first())
    try:
        student.stu_sub = subject_list

        for key in form.keys():
            if hasattr(Students,key):
                setattr(student,key,form[key])

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)

def search_student_db(params_dict):
    paramDict=dict_if(params_dict)
    sqlFilter=Students.query
    if paramDict =={}:
        pagination, user = paginate_html_db(Students)
        return pagination, user

    for key,value in paramDict.items():
        if key=="stu_sub":
            pattern=value.split("-")
            if pattern!=[]:
                sqlFilter=sqlFilter.join(Students.stu_sub).filter(Subjects.subject_name==pattern[0],Subjects.class_name==pattern[1])
        else:
            sqlFilter=sqlFilter.filter(getattr(Students,key)==value)

    result= sqlFilter.all()
    if len(result)==0:
        return None
    return paginate_html_db_select(sqlFilter)


def paginate_html_db(Object,num=14):
    page=request.args.get("page",1,type=int)

    pagination=Object.query.paginate(page,per_page=num,error_out=False)#per_page超出时,error_out=False返回[]
    users=pagination.items
    return pagination,users

def paginate_html_db_select(sqlFilter,num=14):
    page=request.args.get("page",1,type=int)

    pagination=sqlFilter.paginate(page,per_page=num,error_out=False)#per_page超出时,error_out=False返回[]
    users=pagination.items
    return pagination,users


def search_stduent(student_name):
    student=Students.query.filter_by(student_name=student_name).first()
    return student




