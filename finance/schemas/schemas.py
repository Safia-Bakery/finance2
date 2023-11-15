from typing import Optional ,Literal,Dict
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

class SpheresGet(BaseModel):
    name:str
    status:int
    id:int
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

class UserSphereUpdate(BaseModel):
    id:int
    sphere_id:Optional[int]=None
    status:Optional[int]=None
    sequence:Optional[int]=None

class UserSphereFilter(BaseModel):
    id:int
    sphere_id:int
    status:int
    sequence:int
    user_id:int
    user:User
    class Config:
        orm_mode=True

    