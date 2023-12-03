import os
from datetime import datetime,timedelta
from passlib.context import CryptContext
from fastapi import HTTPException, Request
import jwt
from dotenv import load_dotenv

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