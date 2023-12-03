from pydantic import BaseModel

class Admin_Add_Schema(BaseModel):
    id:int
    username:str
    is_active:bool
    is_superuser:bool

class Admin_Show_Schema(Admin_Add_Schema):
    password:str

class login_(BaseModel):
    username:str
    password:str

class create_login_code_schema(BaseModel):
    login_code:int

class enter_to_test(BaseModel):
    name:str
    surname:str
    login_code:str


class ErrorResponse(BaseModel):
    status_code: int
    detail: str

class accept_score_schema(BaseModel):
    id:int
    score:int

class show_to_test(BaseModel):
    id:int
    name:str
    surname:str
    score:int