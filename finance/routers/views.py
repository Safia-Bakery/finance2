from fastapi import APIRouter,BackgroundTasks
from users.utils.user_micro import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from decimal import Decimal
from finance.utils import micro
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

class NoPermissionError(Exception):
    def __init__(self, message="You have no permission to perform this action"):
        self.message = message
        super().__init__(self.message)



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
async def payer_filter(id:Optional[int]=None,name:Optional[str]=None,status:Optional[int]=None,db:Session=Depends(get_db),request_user: User = Depends(get_current_user)):
    return crud.filter_payers(db=db,id=id,name=name,status=status)



@fin_router.post('/v1/image/upload')
async def image_upload(image:list[UploadFile],db:Session=Depends(get_db),request_user: User = Depends(get_current_user)):
    image_list = []
    for i in image:
            #for file in image:
        folder_name = f"files/{micro.generate_random_filename()+i.filename}"
        image_list.append(folder_name)
        with open(folder_name, "wb") as buffer:
            while True:
                chunk = await i.read(1024)
                if not chunk:
                    break
                buffer.write(chunk)

    return {'images':image_list}


@fin_router.post('/v1/orders',response_model=schemas.OrderGet)
async def order_create(form_data:schemas.OrderCreate,db:Session=Depends(get_db),request_user: User = Depends(get_current_user)):
    order = crud.order_create(db=db,form_data=form_data,user_id=request_user.id)
    users = crud.get_sphere_user(db=db,order_id=order.id,sphere_id=order.sphere_id)
    if users:
        crud.history_create(db=db,user_id=users.user_id,order_id=order.id)
    return order

@fin_router.put('/v1/orders',response_model=schemas.OrderGet)
async def order_update(form_data:schemas.OrderUpdate,db:Session=Depends(get_db),request_user: User = Depends(get_current_user)):
    return crud.order_update(db=db,form_data=form_data)

@fin_router.get('/v1/orders',response_model=Page[schemas.OrderGet])
async def order_filter(id:Optional[int]=None,title:Optional[str]=None,price:Optional[Decimal]=None,payer_id:Optional[int]=None,payment_type:Optional[int]=None,supplier:Optional[str]=None,sphere_id:Optional[int]=None,user_id:Optional[int]=None,status:Optional[int]=None,db:Session=Depends(get_db),request_user: User = Depends(get_current_user)):
    orders = crud.order_filter(db=db,id=id,title=title,price=price,payment_type=payment_type,supplier=supplier,sphere_id=sphere_id,payer_id=payer_id,user_id=user_id,status=status,user=request_user)
    print('hell')
    print(orders)
    return paginate(orders)

@fin_router.get('/v1/history',response_model=list[schemas.HistoryGet])
async def history_filter(order_id:int,db:Session=Depends(get_db),request_user: User = Depends(get_current_user)):
    return crud.history_filter(db=db,order_id=order_id)

@fin_router.put('/v1/history',response_model=schemas.HistoryGet)
async def history_update(form_data:schemas.HistoryUpdate,db:Session=Depends(get_db),request_user: User = Depends(get_current_user)):
    is_owner = crud.order_owner_check(db=db,id=form_data.id)
    if is_owner.status!=0 or request_user.id!=is_owner.user_id:
        raise NoPermissionError()
    history = crud.history_update(db=db,form_data=form_data)
    if history:
        if history.status==1:
            users = crud.get_sphere_user(db=db,order_id=history.order_id,sphere_id=history.hi_order.sphere_id)
            if users:
                crud.history_create(db=db,user_id=users.user_id,order_id=history.order_id)
            else:
                crud.order_status_update(db=db,order_id=history.order_id,status=1)
        else:
            crud.order_status_update(db=db,order_id=history.order_id,status=2)
    return history