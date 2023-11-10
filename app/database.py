from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from shared import settings


#! Note: -> my postgres pass has unique characters like @ ! # .... should use quote_plus  !


# SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address/OR/hostname>/<database_name>"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.POSTGRES_HOSTNAME}:%s@{settings.POSTGRES_HOSTNAME}/{settings.POSTGRES_DBNAME}" % quote_plus(settings.POSTGRES_PASSWORD)


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