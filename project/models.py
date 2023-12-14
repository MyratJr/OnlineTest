from sqlalchemy import Column, Integer, String, Boolean, Time
from sqlalchemy.ext.declarative import declarative_base
from datetime import time

Base = declarative_base()


class Admin(Base):
    __tablename__ = "admin"
    id = Column(Integer, primary_key=True,autoincrement=True)
    username = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)


class Students(Base):
    __tablename__="students"
    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    login_code=Column(String,default=0)
    score=Column(Integer)
    registered_time=Column(Time, default=time(13, 00))


class Login_code(Base):
    __tablename__="login_code"
    id = Column(Integer, primary_key=True,autoincrement=True)
    login_code=Column(String,nullable=False)
    expired_time=Column(Time,nullable=False)
    word_box=Column(Integer,nullable=False)
    is_active=Column(Boolean, default=False)