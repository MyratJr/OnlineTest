from typing import List
from fastapi import APIRouter, status, HTTPException
from .schemas import *
from fastapi.responses import JSONResponse
from fastapi_sqlalchemy import db
from .models import Login_code, Students
from .bearer import*
import socket


ip_address = socket.gethostbyname(socket.gethostname())


router=APIRouter(prefix="/admin")


@router.get("/check_lg")
def check_lg():
    check_login_code=db.session.query(Login_code).first()
    if check_login_code is None:
        raise HTTPException(status_code=404, detail=True)
    return {"detail":True}, status.HTTP_200_OK


@router.post("/create_login_code")
def create_login_code(logincode:create_login_code_schema):
    check_login_code=db.session.query(Login_code).first()
    exam_time=time(logincode.hour,logincode.minute)
    if check_login_code is None:
        new_login_code=Login_code(login_code=logincode.login_code, expired_time=exam_time, word_box=logincode.word_group)
        db.session.add(new_login_code)
        db.session.commit()
        return {"detail":"success",
                'login_code':logincode.login_code,
                'Word_boxes':logincode.word_group,
                'expiring time':exam_time
                }
    raise HTTPException(status_code=400, detail="U have a login code before. Use it or delete and create again.")


@router.delete("/delete_login_code")
def delele_login_code():
    check_login_code=db.session.query(Login_code).first()
    all_users_get=db.session.query(Students).all()
    for i in all_users_get:
        db.session.delete(i)
    db.session.delete(check_login_code)
    db.session.commit()
    return {"detail":"success"}


@router.get("/results",response_model=List[Teachers_result])
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