from sqlalchemy import Column, Integer, String, Time
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Students(Base):
    __tablename__="students"
    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    login_code=Column(String,default=0)
    score=Column(Integer)

class Login_code(Base):
    __tablename__="login_code"
    id = Column(Integer, primary_key=True,autoincrement=True)
    login_code=Column(String,nullable=False)
    expired_time=Column(Time,nullable=False)
    word_box=Column(Integer,nullable=False)