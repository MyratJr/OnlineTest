from datetime import timedelta
from fastapi import APIRouter,  Response, status
from .schemas import *
from fastapi.responses import JSONResponse
from fastapi_sqlalchemy import db
from .models import Admin, Login_code, Students
from .bearer import*
import socket
from typing import List


ip_address = socket.gethostbyname(socket.gethostname())


router=APIRouter(prefix="/admin", tags=["admin ALL"])


@router.post("/signup",response_model=List[Admin_Show_Schema_Id], tags=["admin POST"])
def signup(user:Admin_Show_Schema):
    existing_user =db.session.query(Admin).filter_by(username=user.username).first()
    if existing_user:
        exchand(409,"Username already taken")
    else:
        new_user=Admin(
            username=user.username, 
            name=user.firstname, 
            surname=user.surname, 
            hashed_password=hash_password(user.password),
            is_active=user.is_active,
            is_superuser=user.is_superuser
        )
        db.session.add(new_user)
        db.session.commit()
        return db.session.query(Admin).all()


@router.post("/token", tags=["admin POST"])
def login(data:login_1):
    user=db.session.query(Admin).filter_by(username=data.username).first()
    if user is None:
        exchand(401,"Incorrect username")
    if not user.is_active:
        exchand(401, "You have been denied access to login by the superuser")
    if verify_password_(data.password,user):
        access_token=create_access_token(data={"sub":data.username},expires_delta=timedelta(days=30))
        return {
            "id":user.id,
            "username":user.username,
            "is_superuser":user.is_superuser,
            "access_token":access_token,
        }
    else:
        exchand(401,"Incorrect password")
    

@router.put("/change")
def change_admin(name:str, surname:str, old_name:str):
    user=db.session.query(Admin).filter_by(username=old_name).first()
    user.name=name
    user.surname=surname
    db.session.commit()
    return "success"



@router.post("/check_token",response_model=Admin_Add_Schema)
def check_token(schema:Check_token_schema):
    if schema.token:
        user=is_logged_in(schema.token)
        if user:
            user1=db.session.query(Admin).filter_by(username=user).first()
            if user1:
                return user1
    return exchand(404, "Invalid token")


@router.get("/logout", tags=["admin GET"])
def logout(response:Response):
    response.set_cookie(key="Authorization", value="",expires=0)
    return {"message": "Token deleted successfully"}


@router.get("/users",response_model=List[Admin_Add_Schema], tags=["admin GET"])
def users():
    all_users_get=db.session.query(Admin).all()
    return all_users_get


@router.get("/check_lg", tags=["admin GET"])
def check_lg():
    check_login_code=db.session.query(Login_code).first()
    if check_login_code is None:
        exchand(404, False)
    return {"detail":True}, status.HTTP_200_OK


@router.get("/all_login_codes", tags=["admin GET"])
def all_login_codes():
    return db.session.query(Login_code).all()
    

@router.post("/create_login_code", tags=["admin POST"])
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
        return {"id":new_login_code.id,
                'login_code':logincode.login_code,
                'Word_boxes':logincode.word_group,
                'expiring time':exam_time,
                "is_active":logincode.is_active
                }
    exchand(400, f"You have a login code with '{logincode.login_code}' before.")


@router.delete("/delete_login_code/{id}", tags=["admin DELETE"])
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


@router.put("/update_login_code", tags=["admin PUT"])
def update_login_code_(payload:update_login_code):
    check_login_code=db.session.query(Login_code).filter_by(id=payload.id).first()
    if check_login_code is None:
        exchand(404, "No login code found")
    check_login_code.login_code=payload.login_code
    check_login_code.expired_time=time(payload.hour, payload.minute)
    check_login_code.word_box=payload.word_group
    check_login_code.is_active=payload.is_active
    db.session.commit()
    return payload


@router.put("/change_active/{id}/{status}", tags=["admin PUT"])
def change_active(id:int,status:bool):
    check_login_code=db.session.query(Login_code).filter_by(id=id).first()
    check_login_code.is_active=status
    db.session.commit()
    return status

@router.get("/results",response_model=List[Teachers_result], tags=["admin GET"])
def results():
    all_users_get=db.session.query(Students).all()
    return all_users_get


@router.get("/get_result_pdf/{id}", tags=["admin GET"])
def get_result_pdf(id:int):
    exam=db.session.query(Login_code).filter_by(id=id).first()
    if exam is not None:
        pdf=pdf_maker(db.session.query(Students).filter_by(login_code=exam.login_code).order_by(Students.score.desc()).all(),exam)
        return JSONResponse(
            content={"pdf_address": pdf},
            status_code=200,
        )
    exchand(404, "No exam found")


@router.delete("/delete_user/{id}", tags=["admin DELETE"])
def deleteuser(id:int):
    update_score=db.session.query(Students).filter_by(id=id).first()
    if update_score is None:
        exchand(401, "No user found")
    db.session.delete(update_score)
    db.session.commit()
    return {"detail":"Teacher deleted"}


@router.get("/e_e_t/{id}", tags=["admin GET"])
def each_exam_teachers(id:int):
    login_code1=db.session.query(Login_code).filter_by(id=id).first()
    if login_code1 is not None:
        get_teachers=db.session.query(Students).filter_by(login_code=login_code1.login_code).order_by(Students.score.desc()).all()
        for i in get_teachers:
            i.hour=i.registered_time.hour+5
            i.minute=i.registered_time.minute
            i.second=i.registered_time.second
        return get_teachers
    else:
        exchand(404, "No exam found")