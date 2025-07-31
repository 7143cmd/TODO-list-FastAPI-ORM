from sqlalchemy import create_engine, Column, String, TIMESTAMP, BOOLEAN, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
Base = declarative_base()

class PassWRD(Base):
    __tablename__ = 'passWRD'

    id = Column(Integer, primary_key=True, autoincrement=True)
    UserLogin = Column(String)
    UserPassword = Column(String)
    CachedPassword = Column(String)
    TYPE = Column(BOOLEAN)

class Records(Base):
    __tablename__ = 'records'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    context = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.now)
    UserLogin = Column(String)

def DATABASE_CONNECT_USERS():
    engine = create_engine('sqlite:///log.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    
    return Session()

def DATABASE_CONNECT_RECORDS():
    engine = create_engine('sqlite:///records.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    
    return Session()

def REGISTRATION_INSERT(UserPassword, CachedPassword, UserLogin):
    session = DATABASE_CONNECT_USERS()
    
    try:
        new_record = PassWRD(
            UserLogin=UserLogin,
            UserPassword=UserPassword,
            CachedPassword=CachedPassword
        )
        session.add(new_record)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def ADD(Username, title, context):
    session = DATABASE_CONNECT_RECORDS()
    try:
        new_record = Records(
            UserLogin = Username,
            title = title,
            context = context
        )
        session.add(new_record)
        session.commit()
    finally:
        session.close()
def Get_USER(username):
    session = DATABASE_CONNECT_USERS()
    try:
        user = session.query(PassWRD).filter_by(UserLogin=username).first()
        return user
    finally:
        session.close()