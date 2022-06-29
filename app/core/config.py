from dotenv import load_dotenv
from os import environ
from pydantic import BaseSettings
from typing import Optional

DOTENV = '.env'
load_dotenv()
class GlobalConfig(BaseSettings):
    ENV_STATE: Optional[str] = environ['ENV_STATE']
    HOST: Optional[str] = None
    PORT: Optional[int] = None
    TESTTING: bool = True

    class Config:
        env_file = '.env'

class DevConfig(GlobalConfig):
    class Config:
        env_prefix: str = 'DEV_'

class ProdConfig(GlobalConfig):
    TESTTING = False
    class Config:
        env_prefix: str = 'PROD_'