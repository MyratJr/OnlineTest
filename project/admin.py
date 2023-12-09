from datetime import timedelta
from fastapi import APIRouter, Depends, Response
from .schemas import *
from fastapi_sqlalchemy import db
from .models import Admin, Login_code, Students
from .bearer import*

router=APIRouter(prefix="/admin")


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

@router.post("/token")
def login(response:Response,data:login_,is_logged:bool=Depends(is_logged_in)):
    if is_logged:
        exchand(403,"You are already logged in. Please log out before logging in again.")
    user=db.session.query(Admin).filter_by(username=data.username).first()
    if user is None:
        exchand(401,"Incorrect username or password")
    if verify_password_(data.password,user):
        access_token=create_access_token(response,data={"sub":data.username},expires_delta=timedelta(hours=10))
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
    words_boxes=[logincode.one, logincode.two, logincode.three, logincode.four, logincode.five]
    counter=1000
    needed_box=0
    for i in words_boxes:
        if i is True:
            needed_box=counter
        counter+=1000
    time2=datetime.now()
    q=time2+timedelta(hours=logincode.time.hour, 
                      minutes=logincode.time.minute, 
                      seconds=logincode.time.second)
    if check_login_code is None:
        new_login_code=Login_code(login_code=logincode.login_code, expired_time=q, word_box=needed_box)
        db.session.add(new_login_code)
        db.session.commit()
        return {"detail":"success",'Word_boxes':needed_box}
    return {"detail":"U have a login code before. Use it or delete and create again."}


@router.delete("/delete_login_code")
def delele_login_code():
    check_login_code=db.session.query(Login_code).first()
    db.session.delete(check_login_code)
    db.session.commit()
    return {"detail":"success"}

@router.get("/results",response_model=list[Teachers_result])
def results():
    all_users_get=db.session.query(Students).all()
    return all_users_get
