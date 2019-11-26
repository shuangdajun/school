from app.db_service.students import paginate_html_db
from app.model.Base import db
from app.model.Students import Students
from app.model.Subjects import Subjects
from app.model.Teachers import Teachers
import re

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

        subjects=Subjects.query.filter_by(subject_name=args["delete_Subject"]).all()

        [db.session.delete(subject) for subject in subjects]
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)



def search_subject_db(args, params_dict):
    if params_dict["search_Subject"] == "":
        result = Subjects.query.all()
        pagination, user = paginate_html_db(Subjects)
        return pagination, user
    if Subjects.query.filter_by(subject_name=args.get("search_Subject")).all() == []:
        return None
    return paginate_html_db(Subjects)[0], Subjects.query.filter_by(subject_name=args.get("search_Subject")).all()

def editor_subject_db(args,form):
    subject_name = args["search"]
    result=Subjects.query.filter_by(subject_name=subject_name).first()
    result.sub_tea.teacher_name=form["teacher_name"]
    student_list=[]
    for student in form["student_name"].strip(",").split(","):
        student_list.append(Students.query.filter_by(student_name=student).first())
    if student_list!=result.sub_stu:
        result.sub_stu=student_list

    db.session.commit()