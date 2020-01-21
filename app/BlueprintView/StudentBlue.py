# 搜索学生信息初始页面等
from flask import send_from_directory, request, render_template, redirect, url_for, jsonify, app
from flask_login import login_required, current_user

from app.db_service.students import editor_student_db, add_student_db, paginate_html_db, search_student_db, \
    delete_student_db
from app.model.Students import Students
from app.model.Subjects import Subjects
from app.model.User import permission_required
from app.service.detail_students import export_file, xlsx_upload_student, xlsx_upload, judge_add_student_form

from . import web
import os
@web.route("/Student_info", methods=["GET", "POST"])
@login_required
@permission_required(1005)
def Student_info():
    params_dict=request.args.to_dict()
    if "search_student1" in request.args.to_dict():
        params_dict.pop("page", "")
        result = search_student_db( params_dict)
        if result == None:
            return redirect(url_for("web.Student_info") + "?page=1")

        return render_template('school_tem/students.html', students_modellist=result[1], pagination=result[0],user=current_user,pagination_url=params_dict)

    elif "page" in params_dict and params_dict["page"] != "":
        pagination, students_modellistAll = paginate_html_db(Students, 14)
        return render_template("school_tem/students.html", students_modellist=students_modellistAll,
                               pagination=pagination,user=current_user,pagination_url={})

    return redirect(request.url + "?page=1")

#删除学生
@web.route("/deleteStudent",methods=["POST"])
@login_required
@permission_required(1003)
def deleteStudent():
    delete_student_db(request.form)
    return jsonify("True")

# 添加学生
@web.route("/add_Student", methods=["GET", "POST"])
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
@web.route("/editor_student", methods=["GET", "POST"])
@login_required
@permission_required(1004)
def editor_student():

    if request.method == "POST":
        editor_student_db(request.args, request.form)
        return redirect("/Student_info")
    students_modelSelect = Students.query.filter_by(student_name=request.args.get("search")).first()
    subject_modellist=Subjects.query.all()

    subject_modelforce=[value for value in students_modelSelect.stu_sub]
    return render_template("school_tem/editor_student.html", students_modelSelect=students_modelSelect,
                            subject_modellist=subject_modellist,subject_modelforce=subject_modelforce,user=current_user)


# 上传学生信息
@web.route("/upload_Student", methods=["GET", "POST"])
@login_required
@permission_required(1003)
def upload_Student():
    path = os.getcwd()+os.path.sep+"app"+os.path.sep+"upload"+os.path.sep + request.files["file"].filename
    result = xlsx_upload(request.files["file"], path)  # 格式化并存储数据
    if result is None:
        return "文件未上传"
    xlsx_upload_student(path)
    return "文件上传成功"


# 下载学生信息
@web.route("/export_Student/<path:filename>", methods=["POST", "GET"])
@login_required
@permission_required(1003)
def export_Student(filename):
    path = "app/export/" + filename
    result = export_file(path)
    if result is False:
        return False
    # response = make_response(send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True))
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename + ".xlsx", as_attachment=True)


#
# # select获取subject学科
# @web.route("/selectSubject",methods=["POST"])
# @login_required
# @permission_required(1003)
# def selectSubject():
#     result=list(set([value.subject_name for value in Subjects.query.all()]))
#     return jsonify(result)