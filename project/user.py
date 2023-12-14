from fastapi import APIRouter, HTTPException
from .schemas import enter_to_test, accept_score_schema
from fastapi_sqlalchemy import db
from .models import Students, Login_code
from datetime import datetime

router=APIRouter(prefix="/user")


@router.post("/enter_to_test")
def enter_to_test(user_schema:enter_to_test):
    check_login_code=db.session.query(Login_code).filter_by(login_code=user_schema.login_code).first()
    if check_login_code and check_login_code.is_active:
        new_teacher=Students(
            name=user_schema.name,
            surname=user_schema.surname,
            login_code=user_schema.login_code,
            score=0,
            registered_time=datetime.now()
        )
        db.session.add(new_teacher)
        db.session.commit()
        return {
            "id":new_teacher.id,
            "time":check_login_code.expired_time,
            "word_box":check_login_code.word_box
        }
    else:
        raise HTTPException(status_code=404,detail="No exam found with this logincode")


@router.put("/accept_score")
def accept_score(user:accept_score_schema):
    update_score=db.session.query(Students).filter_by(id=user.id).first()
    if update_score is None:
        raise HTTPException(404,"No user found")
    update_score.score=user.score
    db.session.commit()
    return {"detail":"Teacher score updated"}