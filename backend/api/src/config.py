from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]


env_file = f"{BASE_DIR}/.env"




class Config(BaseSettings):

    DB_URL: str 

    DB_NAME: str 

    DB_LOGIN: str 

    DB_PASSWORD: str 

    class Config:
       env_file = f"{BASE_DIR}/.env"

       
config = Config()
