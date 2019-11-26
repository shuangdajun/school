import json
import os
import requests
import xlwt, xlrd
from flask import flash, redirect, render_template, request, url_for, make_response, send_from_directory, jsonify
from flask_login import login_required, login_user, logout_user
from werkzeug.utils import secure_filename

from app import app, db
from app.db_service.students import editor_student_db, delete_student_db, search_student_db, paginate_html_db, \
    add_student_db, search_stduent
from app.db_service.subjects import delete_subject_db, search_subject_db, add_subject_db, editor_subject_db
from app.db_service.teachers import search_teacher_db, delete_teacher_db, editor_teacher_db, add_teacher_db, \
    search_teacher
from app.model.Prices import Prices
from app.model.Subjects import Subjects

from app.model.Teachers import Teachers

from app.model.Students import Students

from app.service.detail_students import judge_add_student_form, judge_add_teacher_form, judge_add_subject_form, \
    xlsx_upload, xlsx_excel, export_file

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


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = {"username": request.form["username"],
                "password": request.form["password"]}
        print('################', user)
        print(path + "/api/v1/auth/login")
        response = requests.post(path + "/api/v1/auth/login", data=user)

        output = json.loads(response.content)
        if output.get("error"):
            error = output["error"]
        else:
            admin_user_id = output.get("user_id")
            admin_user = User.query.get(int(admin_user_id))
            login_user(admin_user)
            return redirect(url_for('index'))

    return render_template('login.html', title='Login', error=error)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    message = "Successfully logged out."
    return render_template('login.html', title='Login', message=message)


# @app.route('/dashboard', methods=['GET', 'POST'])
# @login_required
# def dashboard():
#     students = Student.query.all()
#     teachers = Teacher.query.all()
#     subjects = Subject.query.all()
#     return render_template('dashboard.html', title='Dashboard',
#                            students=students, teachers=teachers,
#                            subjects=subjects)
@app.route('/index.html', methods=['GET', 'POST'])
# @login_required
def dashboard():
    return render_template('school_tem/index.html', title='Dashboard')


# 搜索、删除、学生信息初始页面等
@app.route("/Student_info", methods=["GET", "POST"])
def Student_info():
    params_dict = request.args.to_dict()
    if "page" in params_dict and params_dict["page"] != "":
        pagination, students_modellistAll = paginate_html_db(Students, 14)
        return render_template("school_tem/students.html", students_modellist=students_modellistAll,
                               pagination=pagination)
    elif "search_student" in request.args.to_dict():
        result = search_student_db(request.args, params_dict)
        if result == None:
            return redirect(url_for("Student_info") + "?page=1")

        return render_template('school_tem/students.html', students_modellist=result[1], pagination=result[0])
    elif "delete_student" in params_dict and params_dict["delete_student"] != "":
        delete_student_db(request.args)
        return redirect("/Student_info")


    return redirect(request.url + "?page=1")



# 添加学生
@app.route("/add_Student", methods=["GET", "POST"])
def add_Student():
    if request.method == "POST":
        result = judge_add_student_form(request.form)
        if result[0] == False:
            print(result[1].errors)
            return render_template("school_tem/error.html", errors=result[1].errors)
        subjectList=request.form.getlist("subjectSelect")
        add_student_db(result[1].data.items(),subjectList)

        return redirect("/Student_info")
    subject_modellist = Subjects.query.all()
    return render_template("school_tem/add_students.html",subject_modellist=subject_modellist)


# 编辑学生信息
@app.route("/editor_student", methods=["GET", "POST"])
def editor_student():

    if request.method == "POST":
        editor_student_db(request.args, request.form)
        return redirect("/Student_info")
    students_modelSelect = Students.query.filter_by(student_name=request.args.get("search")).first()
    subject_modellist=Subjects.query.all()
    subject_modelforce = [value for value in students_modelSelect.stu_sub]

    return render_template("school_tem/editor_student.html", students_modelSelect=students_modelSelect,
                            subject_modellist=subject_modellist,subject_modelforce=subject_modelforce)


# 上传学生信息
@app.route("/upload_Student", methods=["GET", "POST"])
def upload_Student():
    path = "app/upload/" + request.files["file"].filename
    result = xlsx_upload(request.files["file"], path)  # 格式化并存储数据
    if result is None:
        return "文件未上传"
    xlsx_excel(path, Students)
    return "文件上传成功"


# 下载学生信息
@app.route("/export_Student/<path:filename>", methods=["POST", "GET"])
def export_Student(filename):
    path = "app/export/" + filename
    result = export_file(path)
    if result is False:
        return False
    # response = make_response(send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True))
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename + ".xlsx", as_attachment=True)


# 搜索、删除、教师信息初始页面等
@app.route("/Teacher_info", methods=["GET", "POST"])
def Teacher_info():
    params_dict = request.args.to_dict()
    if "page" in params_dict and params_dict["page"] != "":
        pagination, teachers_modellistAll = paginate_html_db(Teachers, 14)
        return render_template("school_tem/teachers.html", teachers_modellist=teachers_modellistAll,
                               pagination=pagination)
    elif "search_teacher" in request.args.to_dict():
        result = search_teacher_db(request.args, params_dict)
        if result == None:
            return redirect(url_for("Teacher_info") + "?page=1")
        return render_template('school_tem/teachers.html', teachers_modellist=result[1], pagination=result[0])
    elif "delete_teacher" in params_dict and params_dict["delete_teacher"] != "":
        delete_teacher_db(request.args)
        return redirect("/Teacher_info")

    return redirect(request.url + "?page=1")

    # return render_template('school_tem/teachers.html', students_modellist=students_modellistAll, page=request.args.to_dict()["page"])


# 添加教师
@app.route("/add_Teacher", methods=["GET", "POST"])
def add_Teacher():
    if request.method == "POST":
        result = judge_add_teacher_form(request.form)
        if result[0] == False:
            print(result[1].errors)
            return render_template("school_tem/error.html", errors=result[1].errors)
        subjectList = request.form.getlist("subjectSelect")
        add_teacher_db(result[1].data.items(),subjectList)

        return redirect("/Teacher_info")
    subject_modellist=Subjects.query.all()
    return render_template("school_tem/add_teachers.html",subject_modellist=subject_modellist)


# 编辑教师信息
@app.route("/editor_Teacher", methods=["GET", "POST"])
def editor_teacher():
    if request.method == "POST":
        editor_teacher_db(request.args, request.form)
        return redirect("/Teacher_info")
    teachers_modellistSelect = Teachers.query.filter_by(teacher_name=request.args.get("search")).first()
    subject_modellist=Subjects.query.all()
    subject_modelforce = [value for value in teachers_modellistSelect.tea_sub]
    return render_template("school_tem/editor_teacher.html", teachers_modelSelect=teachers_modellistSelect,teachers_modellistSelect=teachers_modellistSelect,
                           subject_modellist=subject_modellist,subject_modelforce=subject_modelforce)


#
# 上传教师信息
@app.route("/upload_Teacher", methods=["GET", "POST"])
def upload_Teacher():
    path = "app/upload/" + request.files["file"].filename
    result = xlsx_upload(request.files["file"], path)  # 格式化并存储数据
    if result is None:
        return "文件未上传"
    xlsx_excel(path, Teachers)
    return "文件上传成功"


# 下载教师信息
@app.route("/export_Teacher/<path:filename>", methods=["POST", "GET"])
def export_Teacher(filename):
    path = "app/export/" + filename
    result = export_file(path)
    if result is False:
        return False
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename + ".xlsx", as_attachment=True)


# 搜索、删除、学科信息初始页面等
@app.route("/Subject_info", methods=["GET", "POST"])
def Subject_info():
    params_dict = request.args.to_dict()
    if "page" in params_dict and params_dict["page"] != "":
        pagination, subjects_modellistAll = paginate_html_db(Subjects, 14)
        return render_template("school_tem/subjects.html", subjects_modellist=subjects_modellistAll,
                               pagination=pagination)
    elif "search_Subject" in request.args.to_dict():
        result = search_subject_db(request.args, params_dict)
        if result == None:
            return redirect(url_for("Subject_info") + "?page=1")
        return render_template('school_tem/subjects.html', subjects_modellist=result[1], pagination=result[0])
    elif "delete_Subject" in params_dict and params_dict["delete_Subject"] != "":
        delete_subject_db(request.args)
        return redirect("/Subject_info" + "?page=1")


    return redirect(request.url + "?page=1")


# 添加学科
@app.route("/add_Subject", methods=["GET", "POST"])
def add_Subject():
    if request.method == "POST":
        result = judge_add_subject_form(request.form)
        if result[0] == False:
            print(result[1].errors)
            return render_template("school_tem/error.html", errors=result[1].errors)

        add_subject_db(request.form.to_dict().items())
        return redirect("/Subject_info")
    pagination, subjects_modellistAll = paginate_html_db(Students, 6)

    return render_template("school_tem/add_subjects.html", pagination=pagination)


# 编辑学科信息
@app.route("/editor_Subject", methods=["GET", "POST"])
def editor_Subject():
    if request.method == "POST":
        editor_subject_db(request.args, request.form)
        return redirect("/Subject_info")
    subjects_modelSelect = Subjects.query.filter_by(subject_name=request.args.get("search")).first()
    studentlist = []
    for student in subjects_modelSelect.sub_stu:
        studentlist.append(student.student_name)
    pagination, subjects_modellistAll = paginate_html_db(Students, 6)
    return render_template("school_tem/editor_subjects.html", subjects_modelSelect=subjects_modelSelect,
                           pagination=pagination, studentlist=studentlist)


@app.route("/paginate_Subejct", methods=["POST"])
def paginate_subeject():
    pagination, users = paginate_html_db(Students, 6)
    student_list = []
    for user in users:
        student_list.append(user.student_name)
    return jsonify(student_list)





# 上传学科信息
@app.route("/upload_Subject", methods=["GET", "POST"])
def upload_Subject():
    path = "app/upload/" + request.files["file"].filename
    result = xlsx_upload(request.files["file"], path)  # 格式化并存储数据
    if result is None:
        return "文件未上传"
    xlsx_excel(path, Subjects)
    return "文件上传成功"


# 下载学科信息
@app.route("/export_Subject/<path:filename>", methods=["POST", "GET"])
def export_Subject(filename):
    path = "app/export/" + filename
    result = export_file(path)
    if result is False:
        return False
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename + ".xlsx", as_attachment=True)




@app.route("/forms.html", methods=["GET", "POST"])
def forms_info():
    print(request.method)
    return render_template('school_tem/forms.html')


@app.route("/Price_info",methods=["POST","GET"])
def Price_info():
    params_dict = request.args.to_dict()
    if "page" in params_dict and params_dict["page"] != "":
        pagination, prices_modellistAll = paginate_html_db(Prices, 14)
        return render_template("school_tem/prices.html", prices_modellist=prices_modellistAll,
                               pagination=pagination)
    elif "search_Price" in request.args.to_dict():
        result = search_subject_db(request.args, params_dict)
        if result == None:
            return redirect(url_for("Price_info") + "?page=1")
        return render_template('school_tem/prices.html', subjects_modellist=result[1], pagination=result[0])
    elif "delete_Price" in params_dict and params_dict["delete_Price"] != "":
        delete_subject_db(request.args)
        return redirect("/Price_info" + "?page=1")
    return redirect(request.url + "?page=1")


# 上传缴费信息
@app.route("/upload_Price", methods=["GET", "POST"])
def upload_Price():
    path = "app/upload/" + request.files["file"].filename
    result = xlsx_upload(request.files["file"], path)  # 格式化并存储数据
    if result is None:
        return "文件未上传"
    xlsx_excel(path, Prices)
    return "文件上传成功"