import json
from pathlib import Path
from typing import List , Union

from pydantic import AnyHttpUrl , field_validator
from pydantic_settings import BaseSettings , SettingsConfigDict
from dotenv import load_dotenv

# load_dotenv(dotenv_path = 'app/.env')

with open('secrets.json') as s:
    data = json.load(s)

print(data['BACKEND_CORS_ORIGINS'])

#! NOTE! Remember always put .env file in outermost folder like basicsystem/.env
class Settings(BaseSettings):

    # In summary, Base_Directory is assigned the path of the parent directory two levels above the directory of the current script or module
    Base_Directory: Path = Path(__file__).parent.parent

    POSTGRES_USERNAME: str = data['POSTGRES_USERNAME']
    POSTGRES_PASSWORD: str = data['POSTGRES_PASSWORD']
    POSTGRES_HOSTNAME: str = data['POSTGRES_HOSTNAME']
    POSTGRES_DBNAME: str = data['POSTGRES_DBNAME']

    SECRET_KEY: str = data['SECRET_KEY']
    ALGORITHM: str = data['ALGORITHM']
    ACCESS_TOKEN_EXPIRE_MINUTES: int = data['ACCESS_TOKEN_EXPIRE_MINUTES']

    # BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    BACKEND_CORS_ORIGINS: str = data['BACKEND_CORS_ORIGINS']

    Upload_Dir: Path = Base_Directory / 'Uploads/'

    # @field_validator("BACKEND_CORS_ORIGINS")
    # def assemble_cors_origins( cls , v: Union[str , List[str]] ) -> Union[List[str] , str]:
    #     if isinstance(v , str) and not v.startswith("["):
    #         return [i.strip() for i in v.split(",")]
    #     elif isinstance(v , (list , str)):
    #         return v
    #     raise ValueError(v)

    # class Config:
    #     env_file = '.env'

    # model_config = SettingsConfigDict(env_file = '.env')


# settings = Settings(_env_file = '.env')
settings = Settings()
