from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi import Depends, FastAPI, HTTPException,UploadFile,File,Form,Header,Request,status
from typing import Optional
from config.database import engine
from users.routers.user_router import user_router
from fastapi_pagination import paginate,Page,add_pagination
from finance.models.models import Base
from fastapi.staticfiles import StaticFiles
from finance.routers.views import fin_router

app = FastAPI()
app.title = "Safia FastApi App"
app.version = "0.0.1"
app.include_router(user_router)
app.include_router(fin_router)
Base.metadata.create_all(bind=engine)
app.mount("/files", StaticFiles(directory="files"), name="files")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Home"])
def message():
    """message get method"""
    return HTMLResponse("<h1>Fuck of man!</h1>")



add_pagination(app)
add_pagination(fin_router)
add_pagination(user_router)