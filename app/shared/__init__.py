
from pydantic_settings import BaseSettings , SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

#! NOTE! Remember always put .env file in outermost folder like basicsystem/.env
class Settings(BaseSettings):

    POSTGRES_USERNAME: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOSTNAME: str
    POSTGRES_DBNAME: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # class Config:
    #     env_file = '.env'

    # model_config = SettingsConfigDict(env_file = '.env')


settings = Settings(_env_file = '../.env')
