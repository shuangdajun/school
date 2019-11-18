from app.db_service.students import paginate_html_db
from app.model.Base import db
from app.model.Teachers import Teachers





def add_teacher_db(form_dict):
    teacher = Teachers()
    for key, value in form_dict:
        if hasattr(teacher, key):
            setattr(teacher, key, value)
    try:
        db.session.add(teacher)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
def delete_teacher_db(args):
    db.session.execute('delete from fisher.Teachers where teacher_name="{}"'.format(args["delete_teacher"]))

    db.session.commit()

def editor_teacher_db(args,form):
    teacher_name = args["search"]
    teacher_id = \
    list(db.session.execute('select teacher_id from Teachers where teacher_name="{0}"'.format(teacher_name)))[0]._row[0]
    print(teacher_id)
    print('UPDATE Teachers  set teacher_name="{0}" where teacher_id="{1}";'.format(form["teacher_name"],
                                                                                 teacher_id))
    db.session.execute(
        'UPDATE Teachers  set teacher_name="{0}" where teacher_id="{1}";'.format(form["teacher_name"],
                                                                                 teacher_id))
    db.session.execute(
        'UPDATE Teachers  set teacher_address="{0}" where teacher_id="{1}";'.format(form["teacher_address"],
                                                                                teacher_id))

    db.session.execute(
        'UPDATE Teachers  set teacher_phone="{0}" where teacher_id="{1}";'.format(form["teacher_phone"],
                                                                                  teacher_id))
    db.session.commit()


def search_teacher_db(args,params_dict):
    if params_dict["search_teacher"]=="":
        result = Teachers.query.all()
        pagination, user = paginate_html_db(Teachers)
        return pagination, result
    if Teachers.query.filter_by(teacher_name=args.get("search_teacher")).all()==[]:
        return None
    return paginate_html_db(Teachers)[0],Teachers.query.filter_by(teacher_name=args.get("search_teacher")).all()

def search_teacher(teacher_name):
    teacher=Teachers.query.filter_by(teacher_name=teacher_name).first()
    return teacher