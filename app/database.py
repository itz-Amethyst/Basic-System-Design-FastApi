from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
from os import getenv

load_dotenv()
postgres_username = getenv('POSTGRES_USERNAME')
postgres_pass = getenv('POSTGRES_PASSWORD')
postgres_hostname = getenv('POSTGRES_HOSTNAME')
postgres_databasename = getenv('POSTGRES_DBNAME')

#! Note: -> my postgres pass has unique characters like @ ! # .... should use quote_plus  !


# SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address/OR/hostname>/<database_name>"
SQLALCHEMY_DATABASE_URL = f"postgresql://{postgres_username}:%s@{postgres_hostname}/{postgres_databasename}" % quote_plus(postgres_pass)


#  connect_args={"check_same_thread": False} -> For sqlite db
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()