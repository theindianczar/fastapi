from datetime import time

# from psycopg.rows import dict_row
from psycopg2 import connect
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

# SQLALCHEMY_DATABASE_URL = 'postgressql://<username>:<password>@<ip-address/hostname>/<database_name>'

#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Dementor82%40@localhost:5432/fastapi'

SQLALCHEMY_DATABASE_URL = URL.create ("postgresql+psycopg2",username=settings.database_username, password=settings.database_password,host=settings.database_hostname,port=settings.database_port,database=settings.database_name)


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False,bind=engine,expire_on_commit=False)
Base =declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

while True:
    try:
        conn = connect(host="localhost",dbname='fastapi',user='postgres', password='Dementor82@',cursor_factory=RealDictCursor)
        cursor = conn.cursor() 
        print("db conection was succesful")
        break
    except Exception as error:  # noqa: BLE001
        print("Connection to Db failed")
        print("Error:",time.ctime()+error)
        time.sleep(2)