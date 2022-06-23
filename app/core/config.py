from pydantic import BaseSettings
from typing import Optional
from dotenv import dotenv_values

DOTENV = '.env'

class GlobalConfig(BaseSettings):
    ENV_STATE: Optional[str] = dotenv_values(DOTENV)['ENV_STATE']
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