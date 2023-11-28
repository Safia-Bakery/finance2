from finance.models import models
from sqlalchemy.orm import Session
from typing import Optional
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from uuid import UUID
from sqlalchemy import cast, Date,and_
from finance.schemas import schemas


def create_sphere(db:Session,form_data:schemas.SphereCreate):
    query = models.Spheres(name=form_data.name,status=form_data.status)
    db.add(query)
    db.commit()
    db.refresh(query)
    return query

def filter_sphere(db:Session,id,name,status):
    query= db.query(models.Spheres)
    if id is not None:
        query = query.filter(models.Spheres.id==id)
    if name is not None:
        query = query.filter(models.Spheres.name.ilike(f"%{name}%"))
    if status is not None:
        query = query.filter(models.Spheres.status==status)
    return query.all()

def update_sphere(db:Session,form_data:schemas.SpheresUpdate):
    query = db.query(models.Spheres).filter(models.Spheres.id==form_data.id).first()
    if query:
        if form_data.name is not None:
            query.name = form_data.name
        if form_data.status is not None:
            query.status = form_data.status
        db.commit()
        db.refresh(query)
    return query


def create_sphere_user(db:Session,form_data:schemas.UserSphereCreate):
    query = models.SphereUsers(user_id=form_data.user_id,sphere_id=form_data.sphere_id,status=form_data.status,sequence=form_data.sequence,name=form_data.name,show=form_data.show) 
    db.add(query)
    db.commit()
    db.refresh(query)
    return query

def update_sphere_user(db:Session,form_data:schemas.UserSphereUpdate):
    query = db.query(models.SphereUsers).filter(models.SphereUsers.id==form_data.id).first()
    if query:
        if form_data.sphere_id is not None:
            query.sphere_id=form_data.sphere_id
        if form_data.status is not None:
            query.status = form_data.status
        if form_data.sequence is not None:
            query.sequence = form_data.sequence
        if form_data.name is not None:
            query.name=form_data.name
        if form_data.show is not None:
            query.show=form_data.show
        db.commit()
        db.refresh(query)
    return query

def filter_sphere_user(db:Session,id,user_id,sphere_id,status,sequence,name):
    query = db.query(models.SphereUsers)
    if id is not None:
        query = query.filter(models.SphereUsers.id==id)
    if user_id is not None:
        query = query.filter(models.SphereUsers.user_id==user_id)
    if sphere_id is not None:
        query = query.filter(models.SphereUsers.sphere_id==sphere_id)
    if status is not None:
        query = query.filter(models.SphereUsers.status==status)
    if sequence is not None:
        query = query.filter(models.SphereUsers.sequence==sequence)
    if name is not None:
        query = query.filter(models.SphereUsers.name.ilike(f"%{name}%"))
    return query.all()


def create_payers(db:Session,form_data:schemas.PayerCreate):
    query = models.Payers(name=form_data.name,status=form_data.status)
    db.add(query)
    db.commit()
    db.refresh(query)
    return query

def update_payers(db:Session,form_data:schemas.PayerUpdate):
    query = db.query(models.Payers).filter(models.Payers.id==form_data.id).first()
    if query:
        if form_data.name is not None:
            query.name=form_data.name
        if form_data.status is not None:
            query.status =form_data.status

        db.commit()
        db.refresh(query)
    return query

def filter_payers(db:Session,id,name,status):
    query = db.query(models.Payers)
    if id is not None:
        query = query.filter(models.Payers.id==id)
    if name is not None:
        query = query.filter(models.Payers.name.ilike(f"%{name}%"))
    if status is not None:
        query = query.filter(models.Payers.status==status)
    return query.all()



def order_create(db:Session,form_data:schemas.OrderCreate,user_id):
    query = models.Orders(user_id=user_id,title=form_data.title,price=form_data.price,payment_type=form_data.payment_type,supplier=form_data.supplier,sphere_id=form_data.sphere_id,payer_id=form_data.payer_id,files=form_data.files,purchaser=form_data.purchaser,comment = form_data.comment,is_urgent=form_data.is_urgent)
    db.add(query)
    db.commit()
    db.refresh(query)
    return query

def order_update(db:Session,form_data:schemas.OrderUpdate):
    query = db.query(models.Orders).filter(models.Orders.id==form_data.id).first()
    if query:
        if form_data.title is not None:
            query.title =form_data.title
        if form_data.price is not None:
            query.price = form_data.price
        if form_data.payment_type is not None:
            query.payment_type =form_data.payment_type
        if form_data.supplier is not None:
            query.supplier =form_data.supplier
        if form_data.sphere_id is not None:
            query.sphere_id = form_data.sphere_id
        if form_data.payer_id is not None:
            query.payer_id = form_data.payer_id
        if form_data.files is not None:
            query.files = form_data.files
        if form_data.status is not None:
            query.status=form_data.status
        if form_data.purchaser is not None:
            query.purchaser = form_data.purchaser
        if form_data.is_urgent is not None:
            query.is_urgent = form_data.is_urgent
        if form_data.comment is not None:
            query.comment = form_data.comment
        db.commit()
        db.refresh(query)
    return query


def order_filter(db:Session,purchaser,id,title,price,payment_type,supplier,sphere_id,payer_id,user_id,status,user,is_urgent):
    query = db.query(models.Orders).join(models.History)
    if user.status!=2:
        query = query.filter(models.History.user_id==user.id)
    if id is not None:
        query = query.filter(models.Orders.id==id)
    if title is not None:
        query = query.filter(models.Orders.title.ilike(f"%{title}%"))
    if price is not None:
        query = query.filter(models.Orders.price==price)
    if payment_type is not None:
        query = query.filter(models.Orders.payment_type==payment_type)
    if supplier is not None:
        query = query.filter(models.Orders.supplier.ilike(f"%{supplier}%"))
    if sphere_id is not None:
        query = query.filter(models.Orders.sphere_id==sphere_id)
    if payer_id is not None:
        query =query.filter(models.Orders.payer_id==payer_id)
    if user_id is not None:
        query = query.filter(models.History.user_id==user_id)
    if status is not None:
        query = query.filter(models.Orders.status==status)
    if purchaser is not None:
        query = query.filter(models.Orders.purchaser.ilike(f"%{purchaser}%"))
    if is_urgent is not None:
        query = query.filter(models.Orders.is_urgent == is_urgent)
    return query.all()
    

def get_sphere_user(db:Session,sphere_id,order_id):
    history_query = db.query(models.History).filter(models.History.order_id==order_id).all()
    exist_user_list = [i.user_id for i in history_query]
    query = db.query(models.SphereUsers).filter(and_(models.SphereUsers.sphere_id==sphere_id,~models.SphereUsers.user_id.in_(exist_user_list)))
    return query.order_by(models.SphereUsers.sequence.asc()).first()

def history_create(db:Session,user_id,order_id):
    query = models.History(user_id=user_id,order_id=order_id,status=0)
    db.add(query)
    db.commit()
    db.refresh(query)
    return query

def history_filter(db:Session,order_id):
    query = db.query(models.History).filter(models.History.order_id==order_id).all()
    return query

def history_update(db:Session,form_data:schemas.HistoryUpdate):
    query = db.query(models.History).filter(models.History.id==form_data.id).first()
    if query:
        query.status = form_data.status
        if form_data.comment is not None:
            query.comment =form_data.comment
        db.commit()
        db.refresh(query)
    return query

def order_status_update(db:Session,order_id,status):
    query = db.query(models.Orders).filter(models.Orders.id==order_id).first()
    query.status=status
    db.commit()
    return True

def order_owner_check(db:Session,id,user_id):
    query = db.query(models.History).filter(and_(models.History.order_id==id,models.History.user_id==user_id)).first()
    return query

def order_id_get(db:Session,id):
    query = db.query(models.Orders).filter(models.Orders.id==id).first()
    return query