from sqlalchemy import Column, String,Integer,Date,ForeignKey

from app.model.Base import base, db

to_role_permission=db.Table(
    "to_role_permission",
    Column("id",Integer,autoincrement=True,primary_key=True),
    Column("role_id",Integer,ForeignKey("Role.role_id")),
    Column("perm_id",Integer,ForeignKey("Permission.perm_id"))
)
class Role(base):
    __tablename__="Role"
    role_id=Column(Integer,autoincrement=True,primary_key=True)
    role_name=Column(String(20))
    StartTime=Column(Date)
    StopTime=Column(Date)
    description=Column(String(40))
    role_permission=db.relationship("Permission",secondary=to_role_permission,backref="permission_role",lazy="dynamic")


