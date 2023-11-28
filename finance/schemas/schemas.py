from typing import Optional ,Literal,Dict
from decimal import Decimal
from pydantic import BaseModel,Field
from pydantic import validator
from users.schemas.user_schema import User
from uuid import UUID
from users.schemas.user_schema import User
from datetime import datetime


class SphereCreate(BaseModel):
    name:str
    status:Optional[int]=1
    class Config:
        orm_mode=True



class SpheresUpdate(BaseModel):
    name:Optional[str]=None
    status:Optional[int]=None
    id:int
    class Config:
        orm_mode=True


class UserSphereCreate(BaseModel):
    user_id:int
    sphere_id:int
    status:Optional[int]=1
    sequence:int
    name:Optional[str]=None
    show:Optional[int]=None

class UserSphereUpdate(BaseModel):
    id:int
    sphere_id:Optional[int]=None
    status:Optional[int]=None
    sequence:Optional[int]=None
    name:Optional[str]=None
    show:Optional[int]=None


class UserSphereGet(BaseModel):
    id:int
    sphere_id:int
    status:int
    sequence:int
    user_id:int
    sp_user:User
    name:Optional[str]=None
    show:int
    class Config:
        orm_mode=True

class SpheresGet(BaseModel):
    name:str
    status:int
    id:int
    sphereuser:list[UserSphereGet]=None
    class Config:
        orm_mode=True

class PayerCreate(BaseModel):
    name:str
    status:Optional[int]=1
class PayerUpdate(BaseModel):
    id:int
    name:Optional[str]=None
    status:Optional[int]=None

class PayerGet(BaseModel):
    id:int
    name:str
    status:int
    class Config:
        orm_mode=True

class HistoryGet(BaseModel):
    id:int
    user_id:int
    hi_user:User
    order_id:int
    status:int
    comment:Optional[str]=None
    created_at:datetime
    class Config:
        orm_mode=True

class HistoryUpdate(BaseModel):
    id:int
    comment:Optional[str]=None
    status:int
    @validator('status')
    def validate_status(cls, status):
        if status not in [1,2]:
            raise ValueError("status should be 1 or 2")
        return status

class OrderCreate(BaseModel):
    #user_id:int
    title:Optional[str]=None
    price:Optional[Decimal]=None
    payment_type:Optional[int]=None
    supplier:Optional[str]=None
    sphere_id:int
    payer_id:int
    files:Optional[list[str]]=None
    purchaser:Optional[str]=None
    is_urgent:Optional[int]=None
    comment:Optional[str]=None



class OrderUpdate(BaseModel):
    id:int
    title:Optional[str]=None
    price:Optional[Decimal]=None
    payment_type:Optional[int]=None
    supplier:Optional[str]=None
    sphere_id:Optional[int]=None
    payer_id:Optional[int]=None
    files:Optional[list[str]]=None
    status:Optional[int]=None
    purchaser:Optional[str]=None
    is_urgent:Optional[int]=None
    comment:Optional[str]=None

class OrderGet(BaseModel):
    id:int
    title:Optional[str]=None
    price:Optional[Decimal]=None
    payment_type:Optional[int]=None
    supplier:Optional[str]=None
    sphere_id:Optional[int]=None
    payer_id:Optional[int]=None
    files:Optional[list[str]]=None
    status:Optional[int]=None
    order_sp:Optional[SpheresGet]=None
    order_py:Optional[PayerGet]=None
    created_at:datetime
    order_hi:Optional[list[HistoryGet]]=None
    purchaser:Optional[str]=None
    is_urgent:Optional[int]=None
    comment:Optional[str]=None
    class Config:
        orm_mode=True




