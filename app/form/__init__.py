from flask_wtf import FlaskForm as Formwtf
from wtforms import  StringField, validators, IntegerField, SelectField, PasswordField, TextAreaField, SubmitField,BooleanField
from wtforms.validators import Length, DataRequired, NumberRange, ValidationError
from wtforms import Form
from app.model.Subjects import Subjects


class judgeStuentForm(Form):

    student_name = StringField(validators=[Length(min=1,max=20),DataRequired("请输入正确的学生姓名")])
    student_sex = StringField(validators=[Length(min=1,max=20)])
    student_age = IntegerField(validators=[NumberRange(min=1,max=50),DataRequired("请输入正确的年龄")])
    student_phone =StringField(
        render_kw={"class":"hehe"}
    )

    subjectSelect=StringField()

    description=StringField()
    def validate_student_phone(self,field):
        if not (field.data.isdigit() and len(field.data)==11):
            raise ValidationError("请输入正确的手机号码")


class judgeTeacherForm(Form):
    teacher_name=StringField(validators=[Length(min=1,max=20),DataRequired("请输入正确的学生姓名")])
    teacher_address=StringField(validators=[Length(min=1,max=50),DataRequired("请输入正确的住址信息")])
    teacher_phone=StringField()
    subjectSelect=StringField()
    description=StringField()

    def validate_teacher_phone(self,field):
        if not (field.data.isdigit() and len(field.data)==11):
            raise ValidationError("请输入正确的手机号码")

class judgeSubjectForm(Form):
    subject_name=StringField(validators=[Length(min=1,max=20),DataRequired("请输入正确的学科名称")])
    class_name=StringField()
    description=StringField()
    def validate_subject_name(self,field):
        print(Subjects.query.filter_by(subject_name=field.data))

        if len(Subjects.query.filter_by(subject_name=field.data).all()) !=0:
            raise ValidationError("学科重复输入")



class LoginForm(Formwtf):
    user=StringField(validators=[Length(min=1,max=20),DataRequired("账号不能为空")],default="")
    password=PasswordField(validators=[Length(min=1),DataRequired("密码不能为空")],default="")
    # remember_me=BooleanField(validators=[DataRequired()],default=False)
    login=SubmitField("login")