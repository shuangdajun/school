from flask import request, render_template, redirect, make_response, current_app, url_for, jsonify
from flask_login import login_required, current_user

from app.BlueprintView import web
from app.db_service.students import paginate_html_db
from app.db_service.users import search_user_db, delete_user_db
from app.model.Base import db
from app.model.Role import Role
from app.model.User import User, permission_required
from app.service.detail_students import bytes_str_set


@web.route("/user_Manager",methods=["GET","POST"])
@login_required
@permission_required(1005)
def user_Manager():
    params_dict=request.args.to_dict()
    user_onlinelist = bytes_str_set(current_app.config["USER_STATUS_REDIS"].smembers("user_online"))
    if "search_user1" in request.args.to_dict():
        params_dict.pop("page", "")
        result = search_user_db(params_dict)
        if result == None:
            return redirect(url_for("web.user_Manager") + "?page=1")
        result_list = list(map(
            lambda x: {"user": x.user, "username": x.username, "stopTime": x.stopTime, "role": x.user_role.role_name,
                       "description": x.user_role.description, "status": x.status}, result[1]))
        return render_template("school_tem/user_manager.html", user=current_user, result=result_list, pagination=result[0],
                               user_onlinelist=user_onlinelist,pagination_url=params_dict)

    elif "page" in params_dict and params_dict["page"] != "":
        result=list(map(lambda x:{"user":x.user,"username":x.username,"stopTime":x.stopTime,"role":x.user_role.role_name,"description":x.user_role.description,"status":x.status},User.query.all()))
        pagination=paginate_html_db(User,14)[0]
        res=make_response(render_template("school_tem/user_manager.html",user=current_user,result=result,pagination=pagination,user_onlinelist=user_onlinelist,pagination_url={}))
        return res
    return redirect(request.url + "?page=1")

@web.route("/deleteUser",methods=["POST"])
@login_required
@permission_required(1003)
def deleteUser():
    delete_user_db(request.form.to_dict())
    return jsonify("True")


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

@web.route("/editor_user",methods=["GET","POST"])
@login_required
@permission_required(1004)
def editor_User():

    if request.method == "POST":
        try:
            selectUser=User.query.filter(User.user==request.form["user"]).first()
            selectUser.stopTime=request.form["stopTime"]
            selectUser.status=bool(request.form["status"])
            selectUser.username=request.form["username"]
            selectUser.user_role=Role.query.filter_by(role_name=request.form["permission"]).first()
            db.session.commit()
        except Exception as e:
            print(e)

        return redirect("/user_Manager")

    userSelect = User.query.filter(User.user == request.args["search"]).first()

    return render_template("school_tem/editor_user.html", user=current_user,userSelect=userSelect)


@web.route("/delete_user",methods=["POST"])
@login_required
@permission_required(1003)
def delete_user():
    if "delete_user[]" in request.form.keys():
        for user_name in request.form.getlist("delete_user[]"):
            user=User.query.filter_by(user=user_name).first()
            user.status=False
        db.session.commit()

    return redirect("/user_Manager")