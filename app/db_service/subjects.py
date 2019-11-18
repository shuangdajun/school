from app.db_service.students import paginate_html_db
from app.model.Base import db
from app.model.Students import Students
from app.model.Subjects import Subjects
from app.model.Teachers import Teachers


def add_subject_db(form_dict):
    subject = Subjects()

    for key, value in form_dict:

        if hasattr(subject, key):
            setattr(subject, key, value)
        elif key == "teacher_name":
            teacher = Teachers.query.filter_by(teacher_name=value).all()
            subject.sub_tea = teacher
        elif key == "student_name":
            student = Students.query.filter_by(student_name=value).all()
            subject.sub_stu = student
    try:
        db.session.add(subject)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)


def delete_subject_db(args):
    try:
        db.session.execute('delete from fisher.Subjects where subject_name="{}"'.format(args["delete_Subject"]))
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)


def editor_subject_db(args, form):
    subject_name = args["search"]
    subject_id = \
        list(db.session.execute(
            'select subject_id from fisher.Subjects  where subject_name="{0}"'.format(subject_name)))[0]._row[0]
    print(subject_id)
    print('UPDATE fisher.Subjects  set subject_name="{0}" where subject_id="{1}";'.format(form["teacher_name"],
                                                                                          subject_id))
    # db.session.execute(
    #     'UPDATE fisher.Subjects  set teacher_name="{0}" where subject_id="{1}";'.format(form["teacher_name"],
    #                                                                              subject_id))
    # db.session.execute(
    #     'UPDATE fisher.Subjects  set subject_name="{0}" where subject_id="{1}";'.format(form["teacher_address"],
    #                                                                                 subject_id))
    #
    # db.session.execute(
    #     'UPDATE fisher.Subjects  set teacher_phone="{0}" where subject_id="{1}";'.format(form["teacher_phone"],
    #                                                                               subject_id))
    # db.session.commit()
    subject = Subjects.query.fiter_by(subject_name="subject_name")
    subject.sut_stu


def search_subject_db(args, params_dict):
    if params_dict["search_teacher"] == "":
        result = Subjects.query.all()
        pagination, user = paginate_html_db(Subjects)
        return pagination, result
    if Subjects.query.filter_by(teacher_name=args.get("search_teacher")).all() == []:
        return None
    return paginate_html_db(Subjects)[0], Subjects.query.filter_by(teacher_name=args.get("search_teacher")).all()
