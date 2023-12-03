from fastapi import APIRouter, HTTPException
from .schemas import enter_to_test, show_to_test, accept_score_schema
from fastapi_sqlalchemy import db
from .models import Students, Login_code

router=APIRouter(prefix="/user")

@router.post("/enter_to_test",response_model=show_to_test)
def enter_to_test(user_schema:enter_to_test):
    check_login_code=db.session.query(Login_code).first()
    if check_login_code.login_code==user_schema.login_code:
        new_teacher=Students(
            name=user_schema.name,
            surname=user_schema.surname,
            score=0
        )
        db.session.add(new_teacher)
        db.session.commit()
        return new_teacher
    else:
        raise HTTPException(status_code=404,detail="Invalid login code")

@router.put("/accept_score",response_model=show_to_test)
def accept_score(user:accept_score_schema):
    update_score=db.session.query(Students).filter_by(id=user.id).first()
    if user is None:
        raise HTTPException(401,"Incorrect username or password")
    update_score.score=user.score
    db.session.commit()
    return update_score
