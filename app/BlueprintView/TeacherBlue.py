# 搜索、删除、教师信息初始页面等
from flask import request, send_from_directory, redirect, render_template, jsonify, url_for,app
from flask_login import login_required, current_user

from app.BlueprintView import web
from app.db_service.students import paginate_html_db
from app.db_service.teachers import editor_teacher_db, add_teacher_db, delete_teacher_db, search_teacher_db
from app.model.Subjects import Subjects
from app.model.Teachers import Teachers
from app.model.User import permission_required
from app.service.detail_students import xlsx_upload_teacher, xlsx_upload, export_file, judge_add_teacher_form


@web.route("/Teacher_info", methods=["GET", "POST"])
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
@web.route("/deleteTeacher",methods=["POST"])
@login_required
@permission_required(1007)
def deleteTeacher():
    delete_teacher_db(request.form)
    return jsonify("True")


# 添加教师
@web.route("/add_Teacher", methods=["GET", "POST"])
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
@web.route("/editor_Teacher", methods=["GET", "POST"])
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
@web.route("/upload_Teacher", methods=["GET", "POST"])
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
@web.route("/export_Teacher/<path:filename>", methods=["POST", "GET"])
@login_required
@permission_required(1007)
def export_Teacher(filename):
    path = "app/export/" + filename
    result = export_file(path)
    if result is False:
        return False
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename + ".xlsx", as_attachment=True)
