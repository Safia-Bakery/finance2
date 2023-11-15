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

