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

fin_router = APIRouter()