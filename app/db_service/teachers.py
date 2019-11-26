from app.db_service.students import paginate_html_db
from app.model.Base import db
from app.model.Subjects import Subjects
from app.model.Teachers import Teachers





def add_teacher_db(form_dict,subjectList):
    teacher = Teachers()
    for key, value in form_dict:
        if hasattr(teacher, key):
            setattr(teacher, key, value)
        elif key == "subjectSelect":
            value = Subjects.query.filter(Subjects.subject_name.in_(subjectList)).all()
            setattr(teacher, "tea_sub", value)
    try:
        db.session.add(teacher)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
def delete_teacher_db(args):

    try:
        result=db.session.query(Teachers).filter_by(teacher_name=args["delete_teacher"]).first()
        db.session.delete(result)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
def editor_teacher_db(args,form):
    teacher_name = args["search"]
    teacher=Teachers.query.filter_by(teacher_name=teacher_name).first()
    subject_list=[]
    for subject in form.getlist("subjectSelect"):
        subject_list.append(Subjects.query.filter_by(subject_name=subject).first())
    teacher.tea_sub = subject_list


    try:
        teacher.teacher_name=form["teacher_name"]
        teacher.teacher_address=form["teacher_address"]
        teacher.teacher_phone=form["teacher_phone"]
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)


def search_teacher_db(args,params_dict):
    if params_dict["search_teacher"]=="":
        result = Teachers.query.all()
        pagination, user = paginate_html_db(Teachers)
        return pagination, user
    if Teachers.query.filter_by(teacher_name=args.get("search_teacher")).all()==[]:
        return None
    return paginate_html_db(Teachers)[0],Teachers.query.filter_by(teacher_name=args.get("search_teacher")).all()

def search_teacher(teacher_name):
    teacher=Teachers.query.filter_by(teacher_name=teacher_name).first()
    return teacher