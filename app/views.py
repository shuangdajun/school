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
from app.model.Subjects import Subjects

from app.model.Teachers import Teachers

from app.model.Students import Students
from app.model.User import User

from app.service.detail_students import judge_add_student_form, judge_add_teacher_form, judge_add_subject_form, \
    xlsx_upload, export_file, xlsx_upload_student, xlsx_upload_teacher, xlsx_upload_subject, \
    xlsx_upload_price
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


@app.route("/user_pwd",methods=["GET","POST"])
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

@app.route('/', methods=['GET', 'POST'])
@login_required
@permission_required(1005)
def index_dash():
    return redirect("/index.html")


@app.route('/index.html', methods=['GET', 'POST'])
@login_required
@permission_required(1005)
def dashboard():
    studentlist=Students.query.all()
    teacherlist=Teachers.query.all()
    subjectlist = Subjects.query.all()
    pricewarn=PricesWarn.query.all()
    return render_template('school_tem/index.html', title='星泉艺校', user=current_user, studentlist=studentlist,
                           teacherlist=teacherlist, subjectlist=subjectlist,pricewarn=pricewarn)





# 搜索学生信息初始页面等
@app.route("/Student_info", methods=["GET", "POST"])
@login_required
@permission_required(1005)
def Student_info():
    params_dict = request.args.to_dict()
    if "page" in params_dict and params_dict["page"] != "":
        pagination, students_modellistAll = paginate_html_db(Students, 14)
        return render_template("school_tem/students.html", students_modellist=students_modellistAll,
                               pagination=pagination,user=current_user)
    elif "search_student" in request.args.to_dict():
        result = search_student_db(request.args, params_dict)
        if result == None:
            return redirect(url_for("Student_info") + "?page=1")

        return render_template('school_tem/students.html', students_modellist=result[1], pagination=result[0],user=current_user)

    return redirect(request.url + "?page=1")

#删除学生
@app.route("/deleteStudent",methods=["POST"])
@login_required
@permission_required(1003)
def deleteStudent():
    delete_student_db(request.form)
    return jsonify("True")

# 添加学生

@app.route("/add_Student", methods=["GET", "POST"])
@login_required
@permission_required(1002)
def add_Student():
    if request.method == "POST":
        result = judge_add_student_form(request.form)
        if result[0] == False:
            print(result[1].errors)
            return render_template("school_tem/error.html", errors=result[1].errors,user=current_user)
        subjectList=request.form.getlist("subjectSelect")
        add_student_db(result[1].data.items(),subjectList)

        return redirect("/Student_info")
    subject_modellist = Subjects.query.all()
    return render_template("school_tem/add_students.html",subject_modellist=subject_modellist,user=current_user)


# 编辑学生信息
@app.route("/editor_student", methods=["GET", "POST"])
@login_required
@permission_required(1004)
def editor_student():

    if request.method == "POST":
        editor_student_db(request.args, request.form)
        return redirect("/Student_info")
    students_modelSelect = Students.query.filter_by(student_name=request.args.get("search")).first()
    subject_modellist=Subjects.query.all()
    subject_modelforce = [value for value in students_modelSelect.stu_sub]

    return render_template("school_tem/editor_student.html", students_modelSelect=students_modelSelect,
                            subject_modellist=subject_modellist,subject_modelforce=subject_modelforce,user=current_user)


# 上传学生信息
@app.route("/upload_Student", methods=["GET", "POST"])
@login_required
@permission_required(1003)
def upload_Student():
    path = "app/upload/" + request.files["file"].filename
    result = xlsx_upload(request.files["file"], path)  # 格式化并存储数据
    if result is None:
        return "文件未上传"
    xlsx_upload_student(path)
    return "文件上传成功"


# 下载学生信息
@app.route("/export_Student/<path:filename>", methods=["POST", "GET"])
@login_required
@permission_required(1003)
def export_Student(filename):
    path = "app/export/" + filename
    result = export_file(path)
    if result is False:
        return False
    # response = make_response(send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True))
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename + ".xlsx", as_attachment=True)


# 搜索、删除、教师信息初始页面等
@app.route("/Teacher_info", methods=["GET", "POST"])
@login_required
@permission_required(1009)
def Teacher_info():
    params_dict = request.args.to_dict()
    if "page" in params_dict and params_dict["page"] != "":
        pagination, teachers_modellistAll = paginate_html_db(Teachers, 14)
        return render_template("school_tem/teachers.html", teachers_modellist=teachers_modellistAll,
                               pagination=pagination,user=current_user)
    elif "search_teacher" in request.args.to_dict():
        result = search_teacher_db(request.args, params_dict)
        if result == None:
            return redirect(url_for("Teacher_info") + "?page=1")
        return render_template('school_tem/teachers.html', teachers_modellist=result[1], pagination=result[0],user=current_user)
    # elif "delete_teacher" in params_dict and params_dict["delete_teacher"] != "":
    #     delete_teacher_db(request.args)
    #     return redirect("/Teacher_info")

    return redirect(request.url + "?page=1")


#删除教师
@app.route("/deleteTeacher",methods=["POST"])
@login_required
@permission_required(1007)
def deleteTeacher():
    delete_teacher_db(request.form)
    return jsonify("True")


# 添加教师
@app.route("/add_Teacher", methods=["GET", "POST"])
@login_required
@permission_required(1006)
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
    return render_template("school_tem/add_teachers.html",subject_modellist=subject_modellist,user=current_user)


# 编辑教师信息
@app.route("/editor_Teacher", methods=["GET", "POST"])
@login_required
@permission_required(1008)
def editor_teacher():
    if request.method == "POST":
        editor_teacher_db(request.args, request.form)
        return redirect("/Teacher_info")
    teachers_modellistSelect = Teachers.query.filter_by(teacher_name=request.args.get("search")).first()
    subject_modellist=Subjects.query.all()
    subject_modelforce = [value for value in teachers_modellistSelect.tea_sub]
    return render_template("school_tem/editor_teacher.html", teachers_modelSelect=teachers_modellistSelect,teachers_modellistSelect=teachers_modellistSelect,
                           subject_modellist=subject_modellist,subject_modelforce=subject_modelforce,user=current_user)


#
# 上传教师信息
@app.route("/upload_Teacher", methods=["GET", "POST"])
@login_required
@permission_required(1007)
def upload_Teacher():
    path = "app/upload/" + request.files["file"].filename
    result = xlsx_upload(request.files["file"], path)  # 格式化并存储数据
    if result is None:
        return "文件未上传"
    xlsx_upload_teacher(path)
    return "文件上传成功"


# 下载教师信息
@app.route("/export_Teacher/<path:filename>", methods=["POST", "GET"])
@login_required
@permission_required(1007)
def export_Teacher(filename):
    path = "app/export/" + filename
    result = export_file(path)
    if result is False:
        return False
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename + ".xlsx", as_attachment=True)


# 搜索、学科信息初始页面等
@app.route("/Subject_info", methods=["GET", "POST"])
@login_required
@permission_required(1013)
def Subject_info():
    params_dict = request.args.to_dict()
    if "page" in params_dict and params_dict["page"] != "":
        pagination, subjects_modellistAll = paginate_html_db(Subjects, 14)
        return render_template("school_tem/subjects.html", subjects_modellist=subjects_modellistAll,
                               pagination=pagination,user=current_user)
    elif "search_Subject" in request.args.to_dict():
        result = search_subject_db(request.args, params_dict)
        if result == None:
            return redirect(url_for("Subject_info") + "?page=1")
        return render_template('school_tem/subjects.html', subjects_modellist=result[1], pagination=result[0],user=current_user)
    # elif "delete_Subject" in params_dict and params_dict["delete_Subject"] != "":
    #     delete_subject_db(request.args)
    #     return redirect("/Subject_info" + "?page=1")


    return redirect(request.url + "?page=1")

#删除学科
@app.route("/deleteSubject",methods=["POST"])
@login_required
@permission_required(1011)
def deleteSubject():
    delete_subject_db(request.form)
    return jsonify("True")


# 添加学科
@app.route("/add_Subject", methods=["GET", "POST"])
@login_required
@permission_required(1010)
def add_Subject():
    if request.method == "POST":
        result = judge_add_subject_form(request.form)
        if result[0] == False:
            print(result[1].errors)
            return render_template("school_tem/error.html", errors=result[1].errors,user=current_user)

        add_subject_db(request.form.to_dict().items())
        return redirect("/Subject_info")
    pagination, subjects_modellistAll = paginate_html_db(Students, 6)

    return render_template("school_tem/add_subjects.html", pagination=pagination,user=current_user)


# 编辑学科信息
@app.route("/editor_Subject", methods=["GET", "POST"])
@login_required
@permission_required(1012)
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
                           pagination=pagination, studentlist=studentlist,user=current_user)


@app.route("/paginate_Subejct", methods=["POST"])
@login_required
def paginate_subeject():
    pagination, users = paginate_html_db(Students, 6)
    student_list = []
    for user in users:
        student_list.append(user.student_name)
    return jsonify(student_list)





# 上传学科信息
@app.route("/upload_Subject", methods=["GET", "POST"])
@login_required
@permission_required(1011)
def upload_Subject():
    path = "app/upload/" + request.files["file"].filename
    result = xlsx_upload(request.files["file"], path)  # 格式化并存储数据
    if result is None:
        return "文件未上传"
    xlsx_upload_subject(path)
    return "文件上传成功"


# 下载学科信息
@app.route("/export_Subject/<path:filename>", methods=["POST", "GET"])
@login_required
@permission_required(1011)
def export_Subject(filename):
    path = "app/export/" + filename
    result = export_file(path)
    if result is False:
        return False
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename + ".xlsx", as_attachment=True)




@app.route("/forms.html", methods=["GET", "POST"])
@login_required
def forms_info():
    print(request.method)
    return render_template('school_tem/forms.html',user=current_user)

# 添加费用
@app.route("/add_Price", methods=["GET", "POST"])
@login_required
@permission_required(1014)
def add_Price():
    if request.method == "POST":
        add_price_db(request.form.to_dict().items())
        return redirect("/Price_info")
    pagination = paginate_html_db(Students, 6)[0]
    prices_modellistAll=Prices.query.all()
    return render_template("school_tem/add_prices.html", pagination=pagination,prices_modellist=prices_modellistAll,user=current_user)



@app.route("/Price_info",methods=["POST","GET"])
@login_required
@permission_required(1017)
def Price_info():
    params_dict = request.args.to_dict()
    if "page" in params_dict and params_dict["page"] != "":
        pagination, prices_modellistAll = paginate_html_db(Prices, 14)
        return render_template("school_tem/prices.html", prices_modellist=prices_modellistAll,
                               pagination=pagination,user=current_user)
    elif "search_Price" in request.args.to_dict():
        result = search_price_db(request.args, params_dict)
        if result == None:
            return redirect(url_for("Price_info") + "?page=1")
        return render_template('school_tem/prices.html', prices_modellist=result[1], pagination=result[0],user=current_user)
    elif "delete_Price" in params_dict and params_dict["delete_Price"] != "":
        delete_price_db(request.args)
        return redirect("/Price_info" + "?page=1")
    return redirect(request.url + "?page=1")


#删除学科
@app.route("/deletePrice",methods=["POST"])
@login_required
@permission_required(1015)
def deletePrice():
    delete_price_db(request.form)
    return jsonify("True")

# 编辑缴费信息
@app.route("/editor_Price", methods=["GET", "POST"])
@login_required
@permission_required(1016)
def editor_Price():
    if request.method == "POST":
        editor_price_db(request.args, request.form)
        return redirect("/Price_info")
    prices_modelSelect = Prices.query.filter_by(price_id=request.args.get("search")).first()

    # pagination, subjects_modellistAll = paginate_html_db(Students, 6)
    return render_template("school_tem/editor_prices.html", prices_modelSelect=prices_modelSelect,user=current_user)

# 上传缴费信息
@app.route("/upload_Price", methods=["GET", "POST"])
@login_required
@permission_required(1015)
def upload_Price():
    path = "app/upload/" + request.files["file"].filename
    result = xlsx_upload(request.files["file"], path)  # 格式化并存储数据
    if result is None:
        return "文件未上传"
    xlsx_upload_price(path)
    return "文件上传成功"

# 下载学科信息
@app.route("/export_Price/<path:filename>", methods=["POST", "GET"])
@login_required
@permission_required(1011)
def export_Price(filename):
    path = "app/export/" + filename
    result = export_file(path)
    if result is False:
        return False
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename + ".xlsx", as_attachment=True)

@app.route("/comboSelectStu",methods=["POST"])
@login_required
def comboSelectStu():

    studentList=[]
    student_list=Students.query.all()
    flag=1
    for student in student_list:
        student_dict = {}
        student_dict["desc"]=student.student_name
        student_dict["name"]=student.student_name
        student_dict["id"]=flag

        studentList.append(student_dict)
        flag = flag + 1

    return jsonify(studentList)
@app.route("/comboSelectTea",methods=["POST"])
@login_required
def comboSelectTea():

    teacherList=[]
    teacher_list=Teachers.query.all()
    flag=1
    for teacher in teacher_list:
        teacher_dict = {}
        teacher_dict["desc"]=teacher.teacher_name
        teacher_dict["name"]=teacher.teacher_name
        teacher_dict["id"]=flag

        teacherList.append(teacher_dict)
        flag = flag + 1

    return jsonify(teacherList)
@app.route("/comboSelectSub",methods=["POST"])
@login_required
def comboSelectSub():

    subjectList=[]
    subject_list=Subjects.query.all()
    flag=1
    for subject in subject_list:
        subject_dict = {}
        subject_dict["desc"]=subject.subject_name
        subject_dict["name"]=subject.subject_name
        subject_dict["id"]=flag

        subjectList.append(subject_dict)
        flag = flag + 1

    return jsonify(subjectList)
