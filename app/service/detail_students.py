import xlrd, xlwt
import re
from app.model.Base import db
from app.model.Students import Students
from app.model.Subjects import Subjects
from app.model.Teachers import Teachers
from app.view_models.Students import StudentViewModel

from app.form import judgeStuentForm, judgeTeacherForm, judgeSubjectForm


def judge_add_student_form(form_dict):
    judge_formclass = judgeStuentForm(form_dict)
    judge = judge_formclass.validate()

    return [judge, judge_formclass]


def judge_add_teacher_form(form_dict):
    judge_formclass = judgeTeacherForm(form_dict)
    judge = judge_formclass.validate()
    return [judge, judge_formclass]


def judge_add_subject_form(form_dict):
    judge_formclass = judgeSubjectForm(form_dict)
    judge = judge_formclass.validate()
    return [judge, judge_formclass]


def xlsx_upload(file, path):
    if file is None:
        return False
    with open(path, "wb") as f:
        data = file.read()
        f.write(data)
        f.close()
    return True


def xlsx_excel(path, Object):
    workbook = xlrd.open_workbook(path)
    sheet = workbook.sheet_by_name("Sheet1")
    field = [sheet.cell_value(0, i) for i in range(sheet.ncols)]
    object = []

    for row in range(1, sheet.nrows):
        ss = Object()
        for col in range(0, sheet.ncols):
            setattr(ss, field[col], sheet.cell_value(row, col))
            object.append(ss)
    try:
        db.session.add_all(object)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)

    pass


def export_file(filename):
    if re.search("Students_info", filename):
        result = export_db(Students, filename, "student")
    elif re.search("Teachers_info", filename):
        result = export_db(Teachers, filename, "teacher")
    elif re.search("Subjects_info", filename):
        result = export_db(Subjects, filename, "subject")
    else:
        return False
    return result


def export_db(Object, path, patter):
    workbook = xlwt.Workbook(encoding="utf-8")
    sheet = workbook.add_sheet("Sheet1")
    students = Object.query.all()
    rows = len(students)
    field = [value for value in Object.__dict__ if
             re.search("{}_(.*)".format(patter), value) and value != "{}_id".format(patter)]

    try:
        for col in range(0, len(field)):
            sheet.write(0, col, field[col])
        for row in range(1, rows):
            for col in range(0, len(field)):
                sheet.write(row, col, getattr(students[row], field[col]))
        workbook.save(path + ".xlsx")
    except Exception as e:
        return False
    return True
