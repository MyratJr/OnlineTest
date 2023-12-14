from fastapi_sqlalchemy import db
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import os
from datetime import datetime,timedelta
from passlib.context import CryptContext
from fastapi import HTTPException, Request
import jwt
from dotenv import load_dotenv
from .models import Login_code


load_dotenv('.env')


def exchand(status_c, detail_c):
    raise HTTPException(status_c ,detail_c)


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password):
    return password_context.hash(password)


def get_username_from_token(token):
    try:
        decoded_token = jwt.decode(token,os.environ['JWT_SECRET_KEY'], os.environ['ALGORITHM'])
        username = decoded_token["sub"]
        return username
    except jwt.exceptions.DecodeError:
        return exchand(401,"Invalid token")
    except jwt.exceptions.ExpiredSignatureError:
        return exchand(401,"Token has expired")


def is_logged_in(request:Request):
    authorization = request.cookies.get("Authorization")
    if authorization:
        if authorization.startswith("Bearer "):
            token = authorization.split("Bearer ")[1]
            return(get_username_from_token(token))
        else:
            return exchand(401,"Unknown token")
    else:
        return False


def verify_password_(password,user):
    try:
        password_check=password_context.verify(password, user.hashed_password)
        return password_check
    except:
        return False


def create_access_token(response,data:dict,expires_delta:timedelta):
    to_encode=data.copy()
    expire=datetime.utcnow()+expires_delta
    to_encode.update({'exp':expire})
    encoded_jwt=jwt.encode(to_encode, os.environ['JWT_SECRET_KEY'], os.environ['ALGORITHM'])
    response.set_cookie(key="Authorization", value="Bearer "+encoded_jwt)
    return "Bearer "+encoded_jwt


def pdf_maker(items):
    check_login_code=db.session.query(Login_code).first()
    c=canvas.Canvas("static/Exam_results.pdf")
    c.setFont("Helvetica", 22)
    c.setFillColorRGB(0, 0, 255)
    c.drawString(160,800, "Mugallymlaryn synag netijesi")
    c.drawImage("images/logo.png", 0.3 * cm, 27 * cm, width=2.5 * cm, height=2.5 * cm)
    c.setFont("Helvetica", 12)
    c.setFillColorRGB(0, 0, 255)    
    c.drawString(100,760, "T/b")
    c.drawString(140,760, "Ady")
    c.drawString(290,760, "Familiýasy")
    c.drawString(440,760, "Baly")
    c.setFillColorRGB(0, 0, 0)    
    c.drawString(100,755,"_____________________________________________________________" )
    b1=740
    counter_for_new_page=0
    counter=1
    page_counter=1
    c.setFont("Helvetica", 12)
    c.setFillColorRGB(0, 0, 0)
    for i in items:
        if counter_for_new_page==1:
            c.drawString(290,10,f"{page_counter}" )
        counter_for_new_page+=1
        if counter_for_new_page==31:
            counter_for_new_page=1
            page_counter+=1
            c.showPage()
            b1 = 770
        c.drawString(100,b1, f'{counter}')
        c.drawString(140,b1, f"{i.name}")
        c.drawString(290,b1, f"{i.surname}")
        c.drawString(440,b1, f"{i.score}")
        c.drawString(100,b1-5,"_____________________________________________________________" )
        b1=b1-23
        counter+=1
    c.setFont("Helvetica", 12)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(40,70, "Synag wagty")
    gelmesin1=check_login_code.expired_time.hour
    gelsin1=check_login_code.expired_time.minute
    if check_login_code.expired_time.hour<10:
        gelmesin1=f'0{check_login_code.expired_time.hour}'
    if check_login_code.expired_time.minute<10:
        gelmesin1=f'0{check_login_code.expired_time.minute}'
    c.drawString(50,50, f"{gelmesin1}:{gelsin1}")
    c.drawString(250,70, "Sözler toplumy")
    c.drawString(274,50, f"{check_login_code.word_box}")
    c.drawString(460,70, "PDF ýüklenen wagty")
    wagt=datetime.now()
    gelmesin=wagt.hour
    gelsin=wagt.minute
    if wagt.hour<10:
        gelmesin=f'0{wagt.hour}'
    if wagt.minute<10:
        gelsin=f'0{wagt.minute}'
    c.drawString(465,50, f"{wagt.day}.{wagt.month}.{wagt.year} / {gelmesin}:{gelsin}")
    c.save()
    return c._filename