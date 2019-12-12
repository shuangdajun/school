
from flask_login import UserMixin, current_user
from sqlalchemy import Column,String,Integer,Boolean,ForeignKey,Date
from werkzeug.security import generate_password_hash, check_password_hash

from app.model import Permission
from app.model.Base import base, db
from flask import abort
from functools import wraps
def permission_required(permission):

    def wrapfunc(func):
        @wraps(func)
        def decorated(*args,**kwargs):
            if current_user.can(permission)==False:
                abort(403)

            return func(*args,**kwargs)
        return  decorated

    return wrapfunc

class User(UserMixin,base):
    __tablename__="User"
    id=Column(Integer,primary_key=True,autoincrement=True)
    user=Column(String(20),unique=True)
    username=Column(String(20),unique=True)
    password=Column(String(20))
    startTime=Column(Date)
    stopTime=Column(Date)
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




