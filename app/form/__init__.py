from wtforms import Form,StringField,validators,IntegerField,SelectField
from wtforms.validators import Length, DataRequired, NumberRange, ValidationError

from app.model.Students import Students
from app.model.Subjects import Subjects
from app.model.Teachers import Teachers


class judgeStuentForm(Form):

    student_name = StringField(validators=[Length(min=1,max=20),DataRequired("请输入正确的学生姓名")])
    student_sex = StringField(validators=[Length(min=1,max=20)])
    student_age = IntegerField(validators=[NumberRange(min=1,max=50),DataRequired("请输入正确的年龄")])
    student_phone =StringField()
    student_landline = StringField()
    subjectSelect=StringField()
    # def validate_student_name(self,field):
    #     print(Students.query.filter_by(student_name=field.data))
    #
    #     if len(Students.query.filter_by(student_name=field.data).all()) !=0:
    #         raise ValidationError("学生重复输入")

    def validate_student_phone(self,field):
        if not (field.data.isdigit() and len(field.data)==11):
            raise ValidationError("请输入正确的手机号码")
    def validate_student_landline(self,field):
        if not (field.data.isdigit() and len(field.data)==7):
            raise ValidationError("请输入正确的座机号码")

class judgeTeacherForm(Form):
    teacher_name=StringField(validators=[Length(min=1,max=20),DataRequired("请输入正确的学生姓名")])
    teacher_address=StringField(validators=[Length(min=1,max=50),DataRequired("请输入正确的住址信息")])
    teacher_phone=StringField()
    subjectSelect=StringField()
    # def validate_teacher_name(self,field):
    #     print(Teachers.query.filter_by(teacher_name=field.data))
    #
    #     if len(Teachers.query.filter_by(teacher_name=field.data).all()) !=0:
    #         raise ValidationError("学生重复输入")
    def validate_teacher_phone(self,field):
        if not (field.data.isdigit() and len(field.data)==11):
            raise ValidationError("请输入正确的手机号码")

class judgeSubjectForm(Form):
    subject_name=StringField(validators=[Length(min=1,max=20),DataRequired("请输入正确的学科名称")])
    def validate_subject_name(self,field):
        print(Subjects.query.filter_by(subject_name=field.data))

        if len(Subjects.query.filter_by(subject_name=field.data).all()) !=0:
            raise ValidationError("学科重复输入")

