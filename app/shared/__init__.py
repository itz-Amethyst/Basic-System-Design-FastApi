from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from os import getenv

load_dotenv()
class Settings(BaseSettings):
    POSTGRES_USERNAME = getenv('POSTGRES_USERNAME')
    POSTGRES_PASSWORD = getenv('POSTGRES_PASSWORD')
    POSTGRES_HOSTNAME = getenv('POSTGRES_HOSTNAME')
    POSTGRES_DBNAME = getenv('POSTGRES_DBNAME')

    SECRET_KEY = getenv("SECRET_KEY")
    ALGORITHM = getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


settings = Settings(_env_file = ".env")
