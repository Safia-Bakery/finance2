from finance.models import models
from sqlalchemy.orm import Session
from typing import Optional
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from uuid import UUID
from sqlalchemy import cast, Date
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
    query = models.SphereUsers(user_id=form_data.user_id,sphere_id=form_data.sphere_id,status=form_data.status,sequence=form_data.sequence) 
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
        db.commit()
        db.refresh(query)
    return query

def filter_sphere_user(db:Session,id,user_id,sphere_id,status,sequence):
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

