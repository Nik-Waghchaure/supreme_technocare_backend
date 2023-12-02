from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os


load_dotenv()  
Base = declarative_base()


# D:\INTERN\PREFECT\ari.db

def get_db():
    # url = "sqlite:///" + "D:/INTERN/PREFECT/ari.db"
    url ="sqlite:///./ari.db"
    # url = 'D:/INTERN/PREFECT/ari.db'
    # Create engine
    engine = create_engine(url)
    Base.metadata.create_all(bind=engine)
    # Create Session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
