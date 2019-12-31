from sqlalchemy import Column, String,Integer,Date

from app.model.Base import base, db


class Permission(base):
    __tablename__="Permission"
    perm_id = Column(Integer, autoincrement=True, primary_key=True)
    perm_name = Column(String(20))


