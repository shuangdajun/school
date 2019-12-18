from flask import render_template, jsonify, make_response, flash, get_flashed_messages,session
from flask_login import logout_user, current_user, login_user, login_required
from werkzeug.utils import redirect

from app.BlueprintView import web
from app.form import LoginForm
from app.model.Base import db
from app.model.Prices_warning import PricesWarn
from app.model.Students import Students
from app.model.Subjects import Subjects
from app.model.Teachers import Teachers
from app.model.User import User, permission_required


@web.route('/logout', methods=['GET', 'POST'])
def logout():
    form = LoginForm()

    logout_user()
    return render_template("school_tem/login.html",form=form,error=get_flashed_messages())



@web.route("/login",methods=["GET","POST"])

def login():
    form=LoginForm()
    if form.validate_on_submit(): # 表示form是POST进来并且已经validate()=true
        user=User.query.filter_by(user=form.user.data,password=form.password.data).first()

        if current_user.is_authenticated==False and user is not None:
            user.token=session["csrf_token"]
            db.session.commit()
            login_user(user,False)

            return redirect("/index.html")

    return render_template("school_tem/login.html",form=form)

@web.route('/', methods=['GET', 'POST'])
@login_required
@permission_required(1005)
def index_dash():
    return redirect("/index.html")


@web.route('/index.html', methods=['GET', 'POST'])

@login_required
@permission_required(1005)
def dashboard():
    studentlist=Students.query.all()
    teacherlist=Teachers.query.all()
    subjectlist = Subjects.query.all()
    pricewarn=PricesWarn.query.all()

    return render_template('school_tem/index.html', title='星泉艺校', user=current_user, studentlist=studentlist,
                           teacherlist=teacherlist, subjectlist=subjectlist,pricewarn=pricewarn)



@web.route("/SubStuCount",methods=["POST"])
def SubStuCount():
    subjectsAll=list(filter(lambda x : len(x.sub_stu)>0,Subjects.query.all()))
    stuCount=Students.query.count()
    result=list(map(lambda x:{"subject_name":x.subject_name,"x":len(x.sub_stu),"y":len(x.sub_stu)*100/stuCount,"sliced":"true","selected":"true"},subjectsAll))
    return jsonify(result)
