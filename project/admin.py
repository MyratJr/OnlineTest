from datetime import timedelta
from fastapi import APIRouter, Depends, Response, status
from .schemas import *
from fastapi.responses import JSONResponse
from fastapi_sqlalchemy import db
from .models import Admin, Login_code, Students
from .bearer import*
import socket


ip_address = socket.gethostbyname(socket.gethostname())


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


@router.get("/check_lg")
def check_lg():
    check_login_code=db.session.query(Login_code).first()
    if check_login_code is None:
        exchand(404, True)
    return {"detail":True}, status.HTTP_200_OK


@router.post("/create_login_code")
def create_login_code(logincode:create_login_code_schema):
    check_login_code=db.session.query(Login_code).filter_by(login_code=logincode.login_code).first()
    if check_login_code is None:
        exam_time=time(logincode.hour,logincode.minute)
        new_login_code=Login_code(
            login_code=logincode.login_code, 
            expired_time=exam_time, 
            word_box=logincode.word_group,
            is_active=logincode.is_active)
        db.session.add(new_login_code)
        db.session.commit()
        return {"detail":"success",
                'login_code':logincode.login_code,
                'Word_boxes':logincode.word_group,
                'expiring time':exam_time,
                "is_active":logincode.is_active
                }
    exchand(400, f"You have a login code with '{logincode.login_code}' before.")


@router.delete("/delete_login_code/{id}")
def delele_login_code(id:int):
    check_login_code=db.session.query(Login_code).filter_by(id=id).first()
    if check_login_code is None:
        exchand(404, "No login code found")
    get_teachers=db.session.query(Students).filter_by(login_code=check_login_code.login_code)
    for i in get_teachers:
        db.session.delete(i)
    db.session.delete(check_login_code)
    db.session.commit()
    return {"detail":"Login code and related teachers deleted"}


@router.get("/logincode")
def logincode():
    return [db.session.query(Login_code).all()]


@router.put("/update_login_code")
def update_login_code(payload:update_login_code):
    check_login_code=db.session.query(Login_code).filter_by(id=payload.id).first()
    if check_login_code is None:
        exchand(404, "No login code found")
    check_login_code.login_code=payload.login_code
    check_login_code.expired_time=time(payload.hour, payload.minute)
    check_login_code.word_box=payload.word_group
    check_login_code.is_active=payload.is_active
    db.session.commit()
    return payload

@router.get("/results",response_model=list[Teachers_result])
def results():
    all_users_get=db.session.query(Students).all()
    return all_users_get


@router.get("/get_result_pdf")
def get_result_pdf():
    pdf=pdf_maker(db.session.query(Students).order_by(Students.score).all())
    pdf_file_address = f"{ip_address}:8000/{pdf}"
    return JSONResponse(
        content={"pdf_address": pdf_file_address},
        status_code=200,
    )


@router.delete("/delete_user/{id}")
def deleteuser(id:int):
    update_score=db.session.query(Students).filter_by(id=id).first()
    if update_score is None:
        exchand(401, "No user found")
    db.session.delete(update_score)
    db.session.commit()
    return {"detail":"Teacher deleted"}