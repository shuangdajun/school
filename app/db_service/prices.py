from app.db_service.students import paginate_html_db
from app.model.Base import db
from app.model.Students import Students
from app.model.Subjects import Subjects
from app.model.Teachers import Teachers
from app.model.Prices import Prices
import re
price_attr=["startTime","stopTime","ClassHours","prices"]


def add_price_db(form_dict):
    price = Prices()
    student_list = []
    for key, value in form_dict:

        if hasattr(price, key):
            setattr(price, key, value)
        elif key == "teacher_name_text":
            teacher = Teachers.query.filter_by(teacher_name=value).first()
            price.pri_tea = teacher
        elif key == "student_name_text":
            student=Students.query.filter_by(student_name=value).first()
            price.pri_stu=student
        elif key == "subject_name_text":
            subject=Subjects.query.filter_by(subject_name=value).first()
            price.pri_sub=subject
    try:
        db.session.add(price)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)


def delete_price_db(args):
    try:
        # db.session.execute('delete from fisher.Subjects where subject_name="{}"'.format(args["delete_Subject"]))

        price = Prices.query.filter_by(price_id=int(args["delete_Price"])).first()

        db.session.delete(price)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)


def search_price_db(args, params_dict):
    if params_dict["search_Price"] == "":
        pagination, user = paginate_html_db(Prices)
        return pagination, user
    result=Students.query.filter_by(student_name=args.get("search_Price")).first()
    if result == None:
        return None
    return paginate_html_db(Prices)[0], result.stu_pri


def editor_price_db(args, form):
    price_id = args["search"]
    result = Prices.query.filter_by(price_id=int(price_id)).first()
    for attr in price_attr:
        setattr(result,attr,form[attr])

    db.session.commit()
