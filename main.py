from fastapi import FastAPI
from project.admin import router as admin_router
from project.user import router as user_router
import os
from fastapi_sqlalchemy import DBSessionMiddleware
from dotenv import load_dotenv

app=FastAPI()

app.include_router(admin_router)
app.include_router(user_router)

load_dotenv('.env')

app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])