import json
from os import environ
from dotenv import load_dotenv
from core.endpoints import USERLOGIN
from schemas.auth_schemas import UserLogin
from common.common_helper import CommonHelper

load_dotenv()
ENDPOINT = environ['SP_HOST_AND_PORT']
LOG_FILENAME = environ["LOG_FILENAME"]

class AuthService:
    def __init__(self):
        pass

    @staticmethod
    def user_login(request: UserLogin):
        myUrl = ENDPOINT + USERLOGIN
        return CommonHelper.post_url(requestUrl=myUrl, params=request)
