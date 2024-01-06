from pydantic import BaseModel, create_model


class Admin_Add_Schema(BaseModel):
    username:str
    name:str
    surname:str
    is_active:bool
    is_superuser:bool


class Admin_Show_Schema(Admin_Add_Schema):
    password : str


class Admin_Show_Schema_Id(Admin_Add_Schema):
    id:int


class login_1(BaseModel):
    username:str
    password:str


class create_login_code_schema(BaseModel):
    admin_id : int
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
    box:int


class Teachers_result(BaseModel):
    id:int
    name:str
    surname:str
    score:int


class Check_token_schema(BaseModel):
    token : str