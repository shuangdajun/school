# 添加费用
from flask import send_from_directory, request, redirect, render_template, jsonify, url_for, app
from flask_login import login_required, current_user

from app.BlueprintView import web
from app.db_service.prices import editor_price_db, delete_price_db, search_price_db, add_price_db
from app.db_service.students import paginate_html_db
from app.model.Prices import Prices
from app.model.Students import Students
from app.model.Subjects import Subjects
from app.model.Teachers import Teachers
from app.model.User import permission_required
from app.service.detail_students import export_file, xlsx_upload, xlsx_upload_price


@web.route("/add_Price", methods=["GET", "POST"])
@login_required
@permission_required(1014)
def add_Price():
    if request.method == "POST":
        add_price_db(request.form.to_dict().items())
        return redirect("/Price_info")
    pagination = paginate_html_db(Students, 6)[0]
    prices_modellistAll=Prices.query.all()
    return render_template("school_tem/add_prices.html", pagination=pagination,prices_modellist=prices_modellistAll,user=current_user)



@web.route("/Price_info",methods=["POST","GET"])
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
@web.route("/deletePrice",methods=["POST"])
@login_required
@permission_required(1015)
def deletePrice():
    delete_price_db(request.form)
    return jsonify("True")

# 编辑缴费信息
@web.route("/editor_Price", methods=["GET", "POST"])
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
@web.route("/upload_Price", methods=["GET", "POST"])
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
@web.route("/export_Price/<path:filename>", methods=["POST", "GET"])
@login_required
@permission_required(1011)
def export_Price(filename):
    path = "app/export/" + filename
    result = export_file(path)
    if result is False:
        return False
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename + ".xlsx", as_attachment=True)
@web.route("/comboSelectSub",methods=["POST"])
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
@web.route("/comboSelectTea",methods=["POST"])
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
@web.route("/comboSelectStu",methods=["POST"])
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


