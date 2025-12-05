# -------------------------------- Python imports ---------------------------
import pathlib

# -------------------------------- FastAPI imports ---------------------------
from pydantic_settings import BaseSettings

# Project Directories
ROOT = pathlib.Path(__file__).resolve().parent


class Settings(BaseSettings):


    HOST :str
    DATABASE :str
    SCHEMA :str
    STAGE :str
    FILE :str
    user :str
    password :str
    account :str
    port :int
    warehouse :str
    role :str
  

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()