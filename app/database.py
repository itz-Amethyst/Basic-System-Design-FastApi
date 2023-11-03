from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
from os import getenv

load_dotenv()
postgres_username = getenv('POSTGRES_USERNAME', default = 'Test')
postgres_pass = getenv('POSTGRES_PASSWORD', default = 'Test')
postgres_hostname = getenv('POSTGRES_HOSTNAME', default = 'Test')
postgres_databasename = getenv('POSTGRES_DBNAME', default = 'Test')

# SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address/OR/hostname>/<database_name>"
SQLALCHEMY_DATABASE_URL = f"postgresql://{postgres_username}:{postgres_pass}@{postgres_hostname}/{postgres_databasename}"


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