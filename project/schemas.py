from pydantic import BaseModel, create_model
from  datetime import time
from .models import Login_code


class Admin_Add_Schema(BaseModel):
    username:str
    is_active:bool
    is_superuser:bool


class Admin_Show_Schema(Admin_Add_Schema):
    password:str


class Admin_Show_Schema_Id(Admin_Add_Schema):
    id:int


class login_(BaseModel):
    username:str
    password:str
    is_superuser:bool
    is_active:bool


class create_login_code_schema(BaseModel):
    login_code:str
    word_group:int
    hour:int
    minute:int
    is_active:bool


class update_login_code(create_login_code_schema):
    id:int


class enter_to_test(BaseModel):
    name:str
    surname:str
    login_code:str



class accept_score_schema(BaseModel):
    id:int
    score:int


class Teachers_result(BaseModel):
    id:int
    name:str
    surname:str
    score:int