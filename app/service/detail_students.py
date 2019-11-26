import xlrd, xlwt
import re
from app.model.Base import db
from app.model.Students import Students, to_stu_sub
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

    result=sheet_operator_price(Object, field, sheet)
    resultNew = []

    if Object==Students:
        stuNameDict={value.student_name:value for value in result}
        stuNameList=[value.student_name for value in Students.query.all()]
        for key,value in stuNameDict.items():
            if key not in stuNameList:
                resultNew.append(value)
    elif Object==Teachers:
        teaNameDict={value.teacher_name:value for value in result}
        teaNameList=[value.teacher_name for value in Teachers.query.all()]
        for key,value in teaNameDict.items():
            if key not in teaNameList:
                resultNew.append(value)
    else:
        resultNew=result
    try:
        db.session.add_all(resultNew)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)

    pass


def export_file(filename):
    if re.search("Students_info", filename):
        result = export_db(Students, filename, "stu")
    elif re.search("Teachers_info", filename):
        result = export_db(Teachers, filename, "tea")
    elif re.search("Subjects_info", filename):
        result = export_db_subject(Subjects, filename, "subject")
    else:
        return False
    return result


def export_db(Object, path, patter):
    workbook = xlwt.Workbook(encoding="utf-8")
    sheet = workbook.add_sheet("Sheet1")
    students = Object.query.all()
    rows = len(students)
    field = [value for value in Object.__dict__ if
             re.search("{}(.*)".format(patter), value) and value != "{}_id".format(patter)]

    try:
        for col in range(0, len(field)):
            sheet.write(0, col, field[col])
        for row in range(1, rows + 1):
            for col in range(0, len(field)):
                if field[col] in ["stu_sub", "tea_sub"]:
                    result = getObjList([value for value in getattr(students[row - 1], field[col])], "subject_name")
                    sheet.write(row, col, result)

                else:
                    sheet.write(row, col, getattr(students[row - 1], field[col]))
        workbook.save(path + ".xlsx")
    except Exception as e:
        return False
    return True


def export_db_subject(Object, path, patter):
    workbook = xlwt.Workbook(encoding="utf-8")
    sheet = workbook.add_sheet("Sheet1")
    students = Object.query.all()
    rows = len(students)

    field = [value for value in Object.__dict__ if
             re.search("__(.*)", value) == None and value != "_sa_class_manager" and value != "{}_id".format(patter)]

    try:
        for col in range(0, len(field)):
            if field[col] == "sub_stu":
                sheet.write(0, col, "student_name")
            elif field[col] == "sub_tea":
                sheet.write(0, col, "teacher_name")
            else:
                sheet.write(0, col, field[col])

        for row in range(1, rows + 1):
            for col in range(0, len(field)):
                data = []
                if field[col] == "sub_stu":

                    for student in getattr(students[row - 1], field[col]):
                        data.append(student.student_name)
                    sheet.write(row, col, data)
                elif field[col] == "sub_tea":
                    for teacher in getattr(students[row - 1], field[col]):
                        data.append(teacher.teacher_name)
                    sheet.write(row, col, data)
                else:
                    sheet.write(row, col, getattr(students[row - 1], field[col]))
        workbook.save(path + ".xlsx")
    except Exception as e:
        return False
    return True


def getObjList(ObjList, attr):
    ObjAttrList = []
    for Obj in ObjList:
        ObjAttrList.append(getattr(Obj, attr))
    return ObjAttrList


def sheet_operator(Object, field, sheet):
    objectList=[]
    if Object != Subjects:
        for row in range(1,sheet.nrows):
            ss = Object()
            for col in range(0, sheet.ncols):
                if field[col] not in ["stu_sub","tea_sub"]:
                    setattr(ss, field[col], sheet.cell_value(row, col))
            objectList.append(ss)


    else:
        for row in range(1, sheet.nrows):
            ss = Object()
            for col in range(0, sheet.ncols):

                if field[col] == "student_name":
                    data = []
                    result = sheet.cell_value(row, col).split(",")

                    for student in result:
                        try:
                            stuSelect=Students.query.filter_by(student_name=student).first()
                            if stuSelect==None:
                                continue
                            data.append(stuSelect)

                        except Exception as e:
                            print(e)
                    setattr(ss, "sub_stu", data)

                elif field[col] == "teacher_name":
                    try:
                        teacher = Teachers.query.filter_by(teacher_name=sheet.cell_value(row, col)).first()
                        if teacher==None:
                            continue
                        setattr(ss, "sub_tea", [teacher])
                    except Exception as e:
                        print(e)
                else:
                    result=Subjects.query.filter_by(subject_name=sheet.cell_value(row, col)).first()
                    if result!=None:
                        db.session.delete(result)
                        db.session.commit()
                    setattr(ss, field[col], sheet.cell_value(row, col))
            objectList.append(ss)
    return objectList


def sheet_operator_price(Object, field, sheet):
    objectList=[]
    if Object != Subjects:
        for row in range(1,sheet.nrows):
            ss = Object()
            for col in range(0, sheet.ncols):
                try:
                    if sheet.cell_value(row, col)=="":
                        continue
                    if field[col] == "student_name":
                        student=Students.query.filter_by(student_name=sheet.cell_value(row, col)).first()
                        setattr(ss, "pri_stu", student)
                    elif field[col] == "teacher_name":
                        teacher = Teachers.query.filter_by(teacher_name=sheet.cell_value(row, col)).first()
                        setattr(ss, "pri_tea", teacher)
                    elif field[col] == "subject_name":
                        subject=Subjects.query.filter_by(subject_name=sheet.cell_value(row, col)).first()
                        setattr(ss, "pri_sub", subject)
                    elif field[col] in ["startTime","stopTime"]:

                        date=xlrd.xldate_as_datetime(sheet.cell_value(row, col),0)
                        setattr(ss, field[col], date)
                    else:
                        setattr(ss, field[col], sheet.cell_value(row, col))
                except Exception as e:
                    print(e)


            objectList.append(ss)


    else:
        for row in range(1, sheet.nrows):
            ss = Object()
            for col in range(0, sheet.ncols):

                if field[col] == "student_name":
                    data = []
                    result = sheet.cell_value(row, col).split(",")

                    for student in result:
                        try:
                            stuSelect=Students.query.filter_by(student_name=student).first()
                            if stuSelect==None:
                                continue
                            data.append(stuSelect)

                        except Exception as e:
                            print(e)
                    setattr(ss, "sub_stu", data)

                elif field[col] == "teacher_name":
                    try:
                        teacher = Teachers.query.filter_by(teacher_name=sheet.cell_value(row, col)).first()
                        if teacher==None:
                            continue
                        setattr(ss, "sub_tea", [teacher])
                    except Exception as e:
                        print(e)
                else:
                    result=Subjects.query.filter_by(subject_name=sheet.cell_value(row, col)).first()
                    if result!=None:
                        db.session.delete(result)
                        db.session.commit()
                    setattr(ss, field[col], sheet.cell_value(row, col))
            objectList.append(ss)
    return objectList