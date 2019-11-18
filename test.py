# -*- coding:utf-8
from sqlalchemy import Column, String, Integer, create_engine, ForeignKey, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


Base=declarative_base()
class User(Base):
    __tablename__="user"
    id=Column(Integer,primary_key=True)
    user_name=Column(String(20))
class Address(Base):
    __tablename__="address"
    add_id = Column(Integer, primary_key=True)
    address=Column(String(30))
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User")

if __name__=="__main__":
    engine=create_engine("mysql+pymysql://root:1qaz@WSX@172.18.1.101/test",connect_args={'charset':'utf8'})
    metadata = MetaData(engine)

    user = Table('user', metadata,
                 Column('id', Integer, primary_key=True),
                 Column('user_name', String(20)))
    address = Table('address', metadata,
                    Column('add_id', Integer, primary_key=True),
                    Column('address', String(30), nullable=False),
                    )

    # metadata.create_all(engine)
    session=sessionmaker(bind=engine)
    user=User()
    user.user_name="张三"
    db=session()
    db.add(user)






