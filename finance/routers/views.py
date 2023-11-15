from fastapi import APIRouter,BackgroundTasks
from users.utils.user_micro import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from uuid import UUID
from datetime import datetime,date
from users.schemas.user_schema import User
from users.utils.user_micro import get_current_user
from typing import Optional,Union
from fastapi import Request,Form,UploadFile,File
import shutil
from fastapi_pagination import paginate,Page,add_pagination
import re
from typing import Annotated
from finance.schemas import schemas
from finance.crud import crud

fin_router = APIRouter()



@fin_router.post('/v1/spheres',response_model=schemas.SpheresGet)
async def create_sphere(form_data:schemas.SphereCreate,db:Session=Depends(get_db),request_user: User = Depends(get_current_user)):
    return crud.create_sphere(db=db,form_data=form_data)

@fin_router.put('/v1/spheres',response_model=schemas.SpheresGet)
async def update_sphere(form_data:schemas.SpheresUpdate,db:Session=Depends(get_db),request_user: User = Depends(get_current_user)):
    return crud.update_sphere(db=db,form_data=form_data)

@fin_router.get('/v1/spheres',response_model=list[schemas.SpheresGet])
async def filter_sphere(id:Optional[int]=None,status:Optional[int]=None,name:Optional[str]=None,db:Session=Depends(get_db),request_user: User = Depends(get_current_user)):
    return crud.filter_sphere(db=db,id=id,status=status,name=name)



@fin_router.post('/v1/spheres/users',response_model=schemas.UserSphereGet)
async def create_sphere_users(form_data:schemas.UserSphereCreate,db:Session=Depends(get_db),request_user: User = Depends(get_current_user)):
    return crud.create_sphere_user(db=db,form_data=form_data)

@fin_router.put('/v1/spheres/users',response_model=schemas.UserSphereGet)
async def udpate_sphere_users(form_data:schemas.UserSphereUpdate,db:Session=Depends(get_db),request_user: User = Depends(get_current_user)):
    return crud.update_sphere_user(db=db,form_data=form_data)

@fin_router.get('/v1/spheres/users',response_model=list[schemas.UserSphereGet])
async def filter_sphere_users(id:Optional[int]=None,sphere_id:Optional[int]=None,user_id:Optional[int]=None,sequence:Optional[int]=None,status:Optional[int]=None,db:Session=Depends(get_db),request_user: User = Depends(get_current_user)):
    return crud.filter_sphere_user(db=db,id=id,user_id=user_id,sphere_id=sphere_id,sequence=sequence,status=status)


@fin_router.post('/v1/payers',response_model=schemas.PayerGet)
async def payers_create(form_data:schemas.PayerCreate,db:Session=Depends(get_db),request_user: User = Depends(get_current_user)):
    return crud.create_payers(db=db,form_data=form_data)

@fin_router.put('/v1/payers',response_model=schemas.PayerGet)
async def payers_update(form_data:schemas.PayerUpdate,db:Session=Depends(get_db),request_user: User = Depends(get_current_user)):
    return crud.update_payers(db=db,form_data=form_data)

@fin_router.get('/v1/payers',response_model=list[schemas.PayerGet])
async def payer_filter(id:Optional[int]=None,name:Optional[str]=None,status:Optional[int]=None,db:Session=Depends(get_db),request_user: User = Depends(get_current_user))