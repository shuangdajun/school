from flask import request

from app import db
from app.model.Students import Students
from app.model.Teachers import Teachers

def add_student_db(form_dict):
    student = Students()
    for key, value in form_dict:
        if hasattr(student, key):
            setattr(student, key, value)
    try:
        db.session.add(student)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)


def delete_student_db(args):
    db.session.execute('delete from fisher.Students where student_name="{}"'.format(args["delete_student"]))

    db.session.commit()

def editor_student_db(args,form):
    student_name = args["search"]
    student_id = \
    list(db.session.execute('select student_id from Students where Student_name="{0}"'.format(student_name)))[0]._row[0]
    print(student_id)
    try:
        db.session.execute(
            'UPDATE Students  set student_name="{0}" where Student_id="{1}";'.format(form["student_name"],
                                                                                     student_id))
        db.session.execute(
            'UPDATE Students  set student_age="{0}" where Student_id="{1}";'.format(form["student_age"],
                                                                                    student_id))
        db.session.execute(
            'UPDATE Students  set student_sex="{0}" where Student_id="{1}";'.format(form["student_sex"],
                                                                                    student_id))

        db.session.execute(
            'UPDATE Students  set student_phone="{0}" where Student_id="{1}";'.format(form["student_phone"],
                                                                                        student_id))
        db.session.execute(
            'UPDATE Students  set student_landline="{0}" where Student_id="{1}";'.format(form["student_landline"],
                                                                                           student_id))
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
    # return db.session.execute("select * from Students")

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
    # sql_select = "select * from Students limit {0},{1}".format(9*(page-1)+1, 9*page)

    pagination=Object.query.paginate(page,per_page=num,error_out=False)#per_page超出时,error_out=False返回[]
    users=pagination.items
    return pagination,users

def search_stduent(student_name):
    student=Students.query.filter_by(student_name=student_name).first()
    return student




