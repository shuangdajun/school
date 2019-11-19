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
    if "search_student" in request.args.to_dict():
        result = search_student_db(request.args, params_dict)
        if result == None:
            return redirect(url_for("Student_info") + "?page=1")

        return render_template('school_tem/students.html', students_modellist=result[1], pagination=result[0])
    elif "delete_student" in params_dict and params_dict["delete_student"] != "":
        delete_student_db(request.args)
        return redirect("/Student_info")
    elif "page" in params_dict and params_dict["page"] != "":
        pagination, students_modellistAll = paginate_html_db(Students, 14)
        return render_template("school_tem/students.html", students_modellist=students_modellistAll,
                               pagination=pagination)

    return redirect(request.url + "?page=1")

    # return render_template('school_tem/students.html', students_modellist=students_modellistAll, page=request.args.to_dict()["page"])


# 添加学生
@app.route("/add_Student", methods=["GET", "POST"])
def add_Student():
    if request.method == "POST":
        result = judge_add_student_form(request.form)
        if result[0] == False:
            print(result[1].errors)
            return render_template("school_tem/error.html", errors=result[1].errors)

        add_student_db(result[1].data.items())

        return redirect("/Student_info")
    return render_template("school_tem/add_students.html")


# 编辑学生信息
@app.route("/editor_student", methods=["GET", "POST"])
def editor_student():
    if request.method == "POST":
        editor_student_db(request.args, request.form)
        return redirect("/Student_info")
    students_modellistSelect = Students.query.filter_by(student_name=request.args.get("search")).all()
    if students_modellistSelect == "" or len(students_modellistSelect) > 1:
        return "搜索结果多个禁止编辑|禁止直接访问"
    return render_template("school_tem/editor_student.html", students_modelSelect=students_modellistSelect[0])


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

    if "search_teacher" in request.args.to_dict():
        result = search_teacher_db(request.args, params_dict)
        if result == None:
            return redirect(url_for("Teacher_info") + "?page=1")
        return render_template('school_tem/teachers.html', teachers_modellist=result[1], pagination=result[0])
    elif "delete_teacher" in params_dict and params_dict["delete_teacher"] != "":
        delete_teacher_db(request.args)
        return redirect("/Teacher_info")
    elif "page" in params_dict and params_dict["page"] != "":
        pagination, teachers_modellistAll = paginate_html_db(Teachers, 14)
        return render_template("school_tem/teachers.html", teachers_modellist=teachers_modellistAll,
                               pagination=pagination)

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

        add_teacher_db(result[1].data.items())

        return redirect("/Teacher_info")
    return render_template("school_tem/add_teachers.html")


# 编辑教师信息
@app.route("/editor_Teacher", methods=["GET", "POST"])
def editor_teacher():
    if request.method == "POST":
        editor_teacher_db(request.args, request.form)
        return redirect("/Teacher_info")
    teachers_modellistSelect = Teachers.query.filter_by(teacher_name=request.args.get("search")).all()
    if teachers_modellistSelect == "" or len(teachers_modellistSelect) > 1:
        return "搜索结果多个禁止编辑|禁止直接访问"
    return render_template("school_tem/editor_teacher.html", teachers_modelSelect=teachers_modellistSelect[0])


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

    if "search_Subject" in request.args.to_dict():
        result = search_subject_db(request.args, params_dict)
        if result == None:
            return redirect(url_for("Subject_info") + "?page=1")
        return render_template('school_tem/subjects.html', subjects_modellist=result[1], pagination=result[0])
    elif "delete_Subject" in params_dict and params_dict["delete_Subject"] != "":
        delete_subject_db(request.args)
        return redirect("/Subject_info" + "?page=1")
    elif "page" in params_dict and params_dict["page"] != "":
        pagination, subjects_modellistAll = paginate_html_db(Subjects, 14)
        print(subjects_modellistAll)
        return render_template("school_tem/subjects.html", subjects_modellist=subjects_modellistAll,
                               pagination=pagination)

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
    studentlist=[]
    for student in subjects_modelSelect.sub_stu:
        studentlist.append(student.student_name)
    pagination, subjects_modellistAll = paginate_html_db(Students, 6)
    return render_template("school_tem/editor_subjects.html", subjects_modelSelect=subjects_modelSelect, pagination=pagination,studentlist=studentlist)



@app.route("/paginate_Subejct", methods=["POST"])
def paginate_subeject():
    pagination, users = paginate_html_db(Students, 6)
    student_list = []
    for user in users:
        student_list.append(user.student_name)
    return jsonify(student_list)

@app.route("/paginate_Teacher", methods=["GET","POST"])
def paginate_Teacher():
    return {"id":1, "text":"hehe"}




@app.route("/forms.html", methods=["GET", "POST"])
def forms_info():
    print(request.method)
    return render_template('school_tem/forms.html')


@app.route('/add-student', methods=['GET', 'POST'])
@login_required
def add_student():
    if request.method == 'POST':
        create_admin_user()
        student = {"first_name": request.form["first_name"],
                   "last_name": request.form["last_name"],
                   "email_address": request.form["email_address"],
                   "major_id": request.form["major"],
                   "minors": request.form["minors"]}
        response = requests.post(path + "/api/v1/students", data=student, headers=get_token())
        output = json.loads(response.text)
        if output.get("error"):
            flash(output["error"], "error")
        else:
            if "error" in output["message"].lower():
                flash(output["message"], "error")
            else:
                flash(output["message"], "success")

        return redirect(url_for('dashboard'))

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

