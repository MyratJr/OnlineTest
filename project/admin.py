from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import timedelta
from fastapi import APIRouter, Depends, Response, Request, Form
from .schemas import *
from fastapi_sqlalchemy import db
from .models import Admin, Login_code
from .bearer import*

router=APIRouter(prefix="/admin")


templates = Jinja2Templates(directory="templates")


@router.get("/administration", response_class=HTMLResponse)
def read_posts(request: Request):
    return templates.TemplateResponse("blog.html", {"request": request, "posts": "Hello"})


@router.post("/signup",response_model=Admin_Add_Schema)
def signup(user:Admin_Show_Schema):
    existing_user =db.session.query(Admin).filter_by(username=user.username).first()
    if existing_user:
        exchand(409,"Username already taken")
    else:
        new_user=Admin(
            id=user.id, 
            username=user.username, 
            hashed_password=hash_password(user.password),
            is_active=user.is_active,
            is_superuser=user.is_superuser
        )
        db.session.add(new_user)
        db.session.commit()
        return user

@router.post("/token/{username}/{password}")
def login(response:Response,username:str,password:str,is_logged:bool=Depends(is_logged_in)):
    if is_logged:
        exchand(403,"You are already logged in. Please log out before logging in again.")
    user=db.session.query(Admin).filter_by(username=username).first()
    print('-->>>>>>',user)
    if user is None:
        exchand(401,"Incorrect username or password")
    if verify_password_(password,user):
        access_token=create_access_token(response,data={"sub":username},expires_delta=timedelta(hours=10))
        return {"access_token":access_token, "token_type":"bearer"}
    else:
        exchand(401,"Incorrect username or password")
    

@router.get("/logout")
def logout(response:Response):
    response.set_cookie(key="Authorization", value="",expires=0)
    return {"message": "Token deleted successfully"}


@router.get("/users",response_model=list[Admin_Add_Schema])
def users():
    all_users_get=db.session.query(Admin).all()
    return all_users_get


@router.post("/create_login_code")
def create_login_code(logincode:create_login_code_schema):
    check_login_code=db.session.query(Login_code).first()
    if check_login_code is None:
        new_login_code=Login_code(login_code=logincode.login_code, is_active=True)
        db.session.add(new_login_code)
        db.session.commit()
        return {"detail":"success"}
    return {"detail":"U have a login code before. Use it or delete and create again."}

@router.delete("/delete_login_code")
def delele_login_code():
    check_login_code=db.session.query(Login_code).first()
    db.session.delete(check_login_code)
    db.session.commit()
    return {"detail":"success"}