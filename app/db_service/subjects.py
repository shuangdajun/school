from app.db_service.students import paginate_html_db, paginate_html_db_select
from app.model.Base import db
from app.model.Students import Students
from app.model.Subjects import Subjects
from app.model.Teachers import Teachers
import re

from app.service.detail_students import dict_if


def add_subject_db(form_dict):
    subject = Subjects()
    student_list=[]
    for key, value in form_dict:

        if hasattr(subject, key):
            setattr(subject, key, value)
        elif key == "teacher_name":
            teacher = Teachers.query.filter_by(teacher_name=value).all()
            subject.sub_tea = teacher
        elif key == "student_name":
            for student in value.split(",") :
                student_list.append(Students.query.filter_by(student_name=student).first())
            subject.sub_stu = student_list
    try:
        db.session.add(subject)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)


def delete_subject_db(args):
    try:
        # db.session.execute('delete from fisher.Subjects where subject_name="{}"'.format(args["delete_Subject"]))

        result=Subjects.query.filter_by(subject_name=args["delete_Subject"]).first()
        for value in result.sub_pri:
            db.session.delete(value)
        db.session.delete(result)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)



def search_subject_db(params_dict):
    paramDict=dict_if(params_dict)
    sqlFilter=Subjects.query
    if paramDict =={}:
        pagination, user = paginate_html_db(Subjects)
        return pagination, user

    for key,value in paramDict.items():
        if key=="sub_stu":
            if value!="":
                sqlFilter=sqlFilter.join(Subjects.sub_stu).filter(Students.student_name==value)
        elif key=="sub_tea":
            if value!="":
                sqlFilter=sqlFilter.join(Subjects.sub_tea).filter(Teachers.teacher_name==value)
        else:
            sqlFilter=sqlFilter.filter(getattr(Subjects,key)==value)

    result= sqlFilter.all()
    if len(result)==0:
        return None
    return paginate_html_db_select(sqlFilter)

def editor_subject_db(args,form):
    subjectClass = args["search"]
    result=Subjects.query.filter(Subjects.subject_name==subjectClass.split("-")[0],Subjects.class_name==subjectClass.split("-")[1]).first()
    result.sub_tea[0].teacher_name=form["teacher_name"]
    result.description=form["description"]
    student_list=[]
    for student in form["student_name"].strip(",").split(","):
        student_list.append(Students.query.filter_by(student_name=student).first())
    if student_list!=result.sub_stu:
        result.sub_stu=student_list

    db.session.commit()

def search_student_subject_db(data):

    return Students.query.filter_by(student_name=data).all()



