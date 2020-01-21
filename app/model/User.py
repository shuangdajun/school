
from flask_login import UserMixin, current_user, logout_user
from sqlalchemy import Column,String,Integer,Boolean,ForeignKey,Date
from werkzeug.security import generate_password_hash, check_password_hash
import redis
from flask import current_app
from app.model.Role import Role
from app.model.Base import base, db
from flask import abort, session, render_template, redirect, jsonify
from functools import wraps
statusTrans=lambda x: True if x else False
def permission_required(permission):

    def wrapfunc(func):
        @wraps(func)
        def decorated(*args,**kwargs):
            if current_user.can(permission)==False:
                abort(403)
            current_app.config["USER_STATUS_REDIS"].sadd("user_online",current_user.user)
            current_app.config["USER_STATUS_REDIS"].expire("user_online",300)
            return func(*args,**kwargs)
        return  decorated

    return wrapfunc

class User(UserMixin,base):
    __tablename__="User"
    id=Column(Integer,primary_key=True,autoincrement=True)
    user=Column(String(20),unique=True)
    username=Column(String(20),unique=True)
    password=Column(String(100))
    stopTime=Column(Date)
    status=Column(Boolean)
    token=Column(String(40))
    role_id=Column(Integer,ForeignKey("Role.role_id"))
    user_role=db.relationship("Role",backref="role_user")

    def can(self,permiss):

        if self.role_id==1 :
            return True
        for permission in self.user_role.role_permission:
            if permission.perm_id==permiss:
                return True
        return  False


    def set_password(self,password):
        self.password=generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password,password)

    def get_id(self):
        return self.token


    def addUser(user,username,password,stopTime,userpermission,status):
        if User.query.filter(User.user==user).all():
            return False
        else:
            try:
                user_db=User()
                user_db.user=user
                user_db.username=username
                user_db.password=generate_password_hash(password)
                user_db.stopTime=stopTime
                user_db.user_role=Role.query.filter(Role.role_name==userpermission).first()
                user_db.status=statusTrans(status)

                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(e)

        return True


