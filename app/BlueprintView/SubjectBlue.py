# 搜索、学科信息初始页面等
from flask import send_from_directory, request, jsonify, redirect, render_template, url_for, app
from flask_login import login_required, current_user

from app.BlueprintView import web
from app.db_service.students import paginate_html_db
from app.db_service.subjects import editor_subject_db, add_subject_db, delete_subject_db, search_subject_db, \
    search_student_subject_db
from app.model.Students import Students
from app.model.Subjects import Subjects
from app.model.User import permission_required
from app.service.detail_students import export_file, xlsx_upload_subject, xlsx_upload, judge_add_subject_form


@web.route("/Subject_info", methods=["GET", "POST"])
@login_required
@permission_required(1013)
def Subject_info():
    params_dict = request.args.to_dict()
    if "search_subject1" in request.args.to_dict():
        params_dict.pop("page", "")
        result = search_subject_db( params_dict)
        if result == None:
            return redirect(url_for("web.Subject_info") + "?page=1")
        return render_template('school_tem/subjects.html', subjects_modellist=result[1], pagination=result[0],user=current_user,pagination_url=params_dict)
    elif "page" in params_dict and params_dict["page"] != "":
        pagination, subjects_modellistAll = paginate_html_db(Subjects, 14)
        return render_template("school_tem/subjects.html", subjects_modellist=subjects_modellistAll,
                               pagination=pagination,user=current_user,pagination_url={})
    # elif "delete_Subject" in params_dict and params_dict["delete_Subject"] != "":
    #     delete_subject_db(request.args)
    #     return redirect("/Subject_info" + "?page=1")


    return redirect(request.url + "?page=1")

#删除学科
@web.route("/deleteSubject",methods=["POST"])
@login_required
@permission_required(1011)
def deleteSubject():
    delete_subject_db(request.form)
    return jsonify("True")


# 添加学科
@web.route("/add_Subject", methods=["GET", "POST"])
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
@web.route("/editor_Subject", methods=["GET", "POST"])
@login_required
@permission_required(1012)
def editor_Subject():
    if request.method == "POST":
        editor_subject_db(request.args, request.form)
        return redirect("/Subject_info")

    subjects_modelSelect = Subjects.query.filter(Subjects.subject_name==request.args.get("search").split("-")[0],Subjects.class_name==request.args.get("search").split("-")[1]).first()
    studentlist = []
    for student in subjects_modelSelect.sub_stu:
        studentlist.append(student.student_name)
    pagination, subjects_modellistAll = paginate_html_db(Students, 6)
    return render_template("school_tem/editor_subjects.html", subjects_modelSelect=subjects_modelSelect,
                           pagination=pagination, studentlist=studentlist,user=current_user)


@web.route("/paginate_Subejct", methods=["POST"])
@login_required
def paginate_subeject():
    pagination, users = paginate_html_db(Students, 6)
    student_list = []
    for user in users:
        student_list.append(user.student_name)
    return jsonify(student_list)





# 上传学科信息
@web.route("/upload_Subject", methods=["GET", "POST"])
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
@web.route("/export_Subject/<path:filename>", methods=["POST", "GET"])
@login_required
@permission_required(1011)
def export_Subject(filename):
    path = "app/export/" + filename
    result = export_file(path)
    if result is False:
        return False
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename + ".xlsx", as_attachment=True)


@web.route("/searchSubejcts",methods=["GET","POST"])
def searchSubejcts():
    result=[]
    if request.method=="POST" and request.form["search_student"]!="":
        result=search_student_subject_db(request.form["search_student"])
    pagination = paginate_html_db(Students, 11)[0]
    return render_template("school_tem/searchSubejects.html",pagination=pagination,search=result)