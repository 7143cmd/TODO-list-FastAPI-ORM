from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class PassWRD(Base):
    __tablename__ = 'passWRD'
    
    UserLogin = Column(String, primary_key=True)
    UserPassword = Column(String)
    CachedPassword = Column(String)


def DATABASE_CONNECT():
    engine = create_engine('sqlite:///log.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    
    return Session()

def INSERT_INTO(UserPassword, CachedPassword, UserLogin):
    session = DATABASE_CONNECT()
    
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


def Get_USER(username):
    session = DATABASE_CONNECT()
    try:
        user = session.query(PassWRD).filter_by(UserLogin=username).first()
        return user
    finally:
        session.close()