from pydantic import BaseSettings
from typing import Optional
from dotenv import dotenv_values

# access dotenv file
DOTENV = '.env'
ENV_FILE = dotenv_values(DOTENV)
SP_HOST_AND_PORT = ENV_FILE['SP_HOST_AND_PORT']
SP_PRICE_SERVER_HOST = ENV_FILE['SP_PRICE_SERVER']
SP_PRICE_SERVER_PORT = int(ENV_FILE['SP_PRICE_SERVER_PORT'])

# defines a config sending back to main.py
class GlobalConfig(BaseSettings):
    ENV_STATE: Optional[str] = ENV_FILE['ENV_STATE']
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