from sqlalchemy import Column, Integer, String,ForeignKey,Float,DateTime,Boolean,BIGINT,Table,VARCHAR,CHAR,ARRAY,JSON,DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import pytz 
from sqlalchemy.dialects.postgresql import UUID
from users.models.models import Base
import uuid


class Spheres(Base):
    __tablename__='spheres'
    id = Column(Integer,primary_key=True,index=True)
    name = Column(VARCHAR(length=200))
    status = Column(Integer,default=0)
    sphereuser=relationship('SphereUsers',back_populates='sphere')
    sp_order = relationship('Orders',back_populates='order_sp')


class SphereUsers(Base):
    __tablename__='sphere_users'
    id=Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey('users.id'))
    sphere_id = Column(Integer,ForeignKey('spheres.id'))
    sphere = relationship('Spheres',back_populates='sphereuser')
    sp_user = relationship('Users',back_populates='user_sp')
    status =Column(Integer,default=0)
    sequence = Column(Integer)


class Payers(Base):
    __tablename__='payers'
    id=Column(Integer,primary_key=True,Integer=True)
    name = Column(VARCHAR(200))
    py_order = relationship('Orders',back_populates='order_py')


class Orders(Base):
    __tablename__='orders'
    id=Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey('users.id'))
    title = Column(String,nullable=True)
    price = Column(DECIMAL(20,5),nullable=True)
    payment_type = Column(Integer,default=0)
    supplier = Column(String,nullable=True)
    sphere_id = Column(Integer,ForeignKey('spheres.id'))
    order_sp = relationship('Spheres',back_populates='sp_order')
    payer_id = Column(Integer,ForeignKey('payers.id'))
    order_py = relationship('Payers',back_populates='py_order')
    files = Column(ARRAY(String),nullable=True)
    order_hi = relationship('History',back_populates='hi_order')
    created_at = Column(DateTime(timezone=True),default=func.now())
    status = Column(Integer,default=0)


class History(Base):
    __tablename__='history'
    id=Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey('users.id'))
    hi_user = relationship('Users',back_populates='user_hi')
    order_id = Column(Integer,ForeignKey('orders.id'))
    hi_order = relationship('Orders',back_populates='order_hi')
    status = Column(Integer)
    comment= Column(String,nullable=True)
    created_at = Column(DateTime(timezone=True),default=func.now())


class Files(Base):
    __tablename__='files'
    id = Column(Integer,primary_key=True,index=True)
    url = Column(String)
    created_at = Column(DateTime(timezone=True),default=func.now())
