from fastapi import APIRouter, HTTPException
from .schemas import enter_to_test, accept_score_schema
from fastapi_sqlalchemy import db
from .models import Students, Login_code
from datetime import datetime
from .bearer import exchand


router=APIRouter(prefix="/user", tags=["User"])


@router.post("/enter_to_test")
def enter_to_test(user_schema:enter_to_test):
    check_login_code=db.session.query(Login_code).filter_by(login_code=user_schema.login_code).first()
    if check_login_code and check_login_code.is_active:
        user2 = db.session.query(Students).filter_by(name=user_schema.name, surname=user_schema.surname).first()
        if not user2 or user2.login_code != check_login_code.login_code:
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
            exchand(403, "U have completed the quiz before. Wait to next quiz.")
    else:
        raise HTTPException(status_code=404,detail="No exam found with this logincode")


@router.put("/accept_score")
def accept_score(user:accept_score_schema):
    box_dict={
        "1000" : 20,
        "2000" : 40,
        "3000" : 60,
        "4000" : 80,
        "5000" : 100
    }
    update_score=db.session.query(Students).filter_by(id=user.id).first()
    if update_score is None:
        raise HTTPException(404,"No user found")
    update_score.score=(user.score*100)/box_dict[str(user.box)]
    db.session.commit()
    return {"detail":"Teacher score updated"}