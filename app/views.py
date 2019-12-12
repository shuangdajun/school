import json
import os
import requests
import xlwt, xlrd
from flask import flash, redirect, render_template, request, url_for, make_response, send_from_directory, jsonify
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.utils import secure_filename

from app import app, db
from app.db_service.prices import search_price_db, editor_price_db, delete_price_db, add_price_db
from app.db_service.students import editor_student_db, delete_student_db, search_student_db, paginate_html_db, \
    add_student_db, search_stduent
from app.db_service.subjects import delete_subject_db, search_subject_db, add_subject_db, editor_subject_db
from app.db_service.teachers import search_teacher_db, delete_teacher_db, editor_teacher_db, add_teacher_db, \
    search_teacher
from app.form import LoginForm
from app.model.Prices import Prices
from app.model.Prices_warning import PricesWarn
from app.model.Role import Role
from app.model.Subjects import Subjects

from app.model.Teachers import Teachers

from app.model.Students import Students
from app.model.User import User

from app.service.detail_students import judge_add_student_form, judge_add_teacher_form, judge_add_subject_form, \
    xlsx_upload, export_file, xlsx_upload_student, xlsx_upload_teacher, xlsx_upload_subject, \
    xlsx_upload_price, SubStuCountDict, SubStuCountFilter
from flask_login import logout_user
from app.model.User import permission_required
from urllib.parse import urljoin,urlparse
if os.getenv("ENVIRONMENT") == "development":
    path = "http://127.0.0.1:5000"
else:
    path = "https://flask-school-app.herokuapp.com"

os.path.join("C:\\flask-school-app-and-api-master\\app\\templates\\school_tem\\bootstrap.css")


def create_admin_user():
    admin = User.query.filter_by(username="admin").first()
    if admin:
        db.session.delete(admin)
        db.session.commit()

    admin = User(username="admin",
                 password="admin1234")
    db.session.add(admin)
    db.session.commit()


def get_token():
    admin = {"username": "admin",
             "password": "admin1234"}
    response = requests.post(path + "/api/v1/auth/login",
                             data=admin)
    output = json.loads(response.text)
    token = output["token"]
    return {"Authorization": token}


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@app.route("/site-map")
def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    # links is now a list of url, endpoint tuples
    print(links)
    return render_template('login.html', title='Login')

#
# @app.route('/', methods=['GET', 'POST'])
# def login():
#     error = None
#     if request.method == 'POST':
#         user = {"username": request.form["username"],
#                 "password": request.form["password"]}
#         print('################', user)
#         print(path + "/api/v1/auth/login")
#         response = requests.post(path + "/api/v1/auth/login", data=user)
#
#         output = json.loads(response.content)
#         if output.get("error"):
#             error = output["error"]
#         else:
#             admin_user_id = output.get("user_id")
#             admin_user = User.query.get(int(admin_user_id))
#             login_user(admin_user)
#             return redirect(url_for('index'))
#
#     return render_template('login.html', title='Login', error=error)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect('/login')



@app.route("/login",methods=["GET","POST"])
def login():
    form=LoginForm()
    if form.validate_on_submit(): # 表示form是POST进来并且已经validate()=true
        user=User.query.filter_by(user=form.user.data,password=form.password.data).first()
        if current_user.is_authenticated==False and user is not None:
            login_user(user,False)
            return redirect("/index.html")

    return render_template("school_tem/login.html",form=form)






@app.route("/forms.html", methods=["GET", "POST"])
@login_required
def forms_info():
    print(request.method)
    return render_template('school_tem/forms.html',user=current_user)





