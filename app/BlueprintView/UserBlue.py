from flask import request, render_template, redirect
from flask_login import login_required, current_user

from app.BlueprintView import web
from app.db_service.students import paginate_html_db
from app.model.Base import db
from app.model.User import User


@web.route("/user_Manager",methods=["GET"])
@login_required
def user_Manager():
    result=list(map(lambda x:{"user":x.user,"username":x.username,"startTime":x.startTime,"stopTime":x.stopTime,"role":x.user_role.role_name,"description":x.user_role.description},User.query.all()))
    pagination=paginate_html_db(User,14)[0]
    return render_template("school_tem/user_manager.html",user=current_user,result=result,pagination=pagination)




@web.route("/user_pwd",methods=["GET","POST"])
@login_required
def user_modify():
    if request.method=="POST":
        current_user.user=request.form["user"]
        current_user.username=request.form["username"]
        current_user.password=request.form["password"]

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
        return redirect("/index.html")
    return render_template("school_tem/password_modify.html",user=current_user)
