from app.db_service.students import paginate_html_db, paginate_html_db_select
from app.model.Base import db
from app.model.User import User,Role
from app.service.detail_students import dict_if


def search_user_db(params_dict):
    paramDict=dict_if(params_dict)
    sqlFilter=User.query
    if paramDict =={}:
        pagination, user = paginate_html_db(User)
        return pagination, user

    for key,value in paramDict.items():
        if key=="description":
            if value!=[]:
                sqlFilter=sqlFilter.join(User.user_role).filter(Role.description==paramDict["description"])
        else:
            sqlFilter=sqlFilter.filter(getattr(User,key)==value)

    result= sqlFilter.all()
    if len(result)==0:
        return None
    return paginate_html_db_select(sqlFilter)
def delete_user_db(args):
    try:
        result=db.session.query(User).filter_by(user=args["delete_user"]).first()
        db.session.delete(result)

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)