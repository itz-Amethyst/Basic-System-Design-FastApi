from urllib.parse import quote_plus

from sqlalchemy import create_engine , MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.shared import settings

#! Note: -> my postgres pass has unique characters like @ ! # .... should use quote_plus  !


# SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address/OR/hostname>/<database_name>"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.POSTGRES_USERNAME}:%s@{settings.POSTGRES_HOSTNAME}/{settings.POSTGRES_DBNAME}" % quote_plus(settings.POSTGRES_PASSWORD)
print(SQLALCHEMY_DATABASE_URL)


#  connect_args={"check_same_thread": False} -> For sqlite db
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Not sure about this

metadata = MetaData()
# metadata.create_all(bind = engine)

Base = declarative_base(metadata = metadata)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()