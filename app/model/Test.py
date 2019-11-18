

from sqlalchemy import Integer, Column, Float, String, ForeignKey, Table
from sqlalchemy.orm import relationship

from app.model.Base import db
association_table = db.Table('association',
                             db.Column('id', db.Integer, primary_key=True, autoincrement=True),
                             db.Column('customer_id', db.Integer, db.ForeignKey('customer.id')),
                             db.Column('product_id', db.Integer, db.ForeignKey('product.id'))
                             )

class Customer(db.Model):
    __tablename__="customer"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name=Column(String(10))
    work=Column(String(10))
    customer_to_product = relationship('Product',
                                          secondary=association_table,
                                          backref='product_to_customer',
                                          lazy='dynamic'
                                          )



class Product(db.Model):
    __tablename__ = 'product'
    id=Column(Integer, primary_key=True, autoincrement=True)
    name=Column(String(10))
    price=Column(Float)

