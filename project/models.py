from sqlalchemy import Column, Integer, String, Boolean, Time
from sqlalchemy.ext.declarative import declarative_base
from datetime import time

Base = declarative_base()


class Admin(Base):
    __tablename__ = "admin"
    id = Column(Integer, primary_key=True,autoincrement=True)
    username = Column(String, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False)
    is_superuser = Column(Boolean, nullable=False)


class Students(Base):
    __tablename__="students"
    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    login_code=Column(String)
    score=Column(Integer)
    registered_time=Column(Time)


class Login_code(Base):
    __tablename__="login_code"
    id = Column(Integer, primary_key=True,autoincrement=True)
    login_code=Column(String,nullable=False)
    created_admin = Column(Integer, nullable=False)
    expired_time=Column(Time,nullable=False)
    word_box=Column(Integer,nullable=False)
    is_active=Column(Boolean)