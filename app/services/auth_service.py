from os import environ
from dotenv import load_dotenv
from schemas.auth_schemas import UserLogin, AccountSumModel
from core.endpoints import USERLOGIN, ACCOUNTINFO
from schemas.auth_schemas import UserLogin
from common.common_helper import CommonHelper

load_dotenv()
ENDPOINT = environ['SP_HOST_AND_PORT']
LOG_FILENAME = environ["LOG_FILENAME"]

class AuthService:
    def __init__(self):
        pass


    @staticmethod # Method is instance method otherwise
    def user_login(request: UserLogin): # Get token for this session
        myUrl = ENDPOINT + USERLOGIN
        res = CommonHelper.post_url(requestUrl=myUrl, params=request)
        return res
        

    @staticmethod
    def get_acc_info(request: AccountSumModel): # Get client information for this session
        accUrl = ENDPOINT + ACCOUNTINFO
        accres = CommonHelper.post_url(requestUrl=accUrl, params=request)
        return accres

