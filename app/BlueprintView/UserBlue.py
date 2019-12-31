from flask import request, render_template, redirect
from flask_login import login_required, current_user

from app.BlueprintView import web
from app.db_service.students import paginate_html_db
from app.model.Base import db
from app.model.User import User, permission_required


@web.route("/user_Manager",methods=["GET"])
@login_required
def user_Manager():
    result=list(map(lambda x:{"user":x.user,"username":x.username,"stopTime":x.stopTime,"role":x.user_role.role_name,"description":x.user_role.description,"status":x.status},User.query.all()))
    pagination=paginate_html_db(User,14)[0]
    return render_template("school_tem/user_manager.html",user=current_user,result=result,pagination=pagination)




@web.route("/user_pwd",methods=["GET","POST"])
@login_required
@permission_required(1004)
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


@web.route("/add_User",methods=["GET","POST"])

@login_required
@permission_required(1002)
def add_User():
    if request.method == "POST":
        result = User.addUser(request.form["user"], request.form["username"], request.form["password"],
                              request.form["stopTime"], request.form["userpermission"], request.form["status"])
        if result:
            return redirect("/user_Manager")
        else:
            return render_template("school_tem/error.html",errors="账号重复创建")
    return render_template("school_tem/add_user.html", user=current_user)
