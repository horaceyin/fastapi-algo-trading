from os import environ
from dotenv import load_dotenv
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from requests import get, post
from schemas.auth_schemas import UserLogin, AccountSumModel
from core.endpoints import USERLOGIN
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
    def acc_login(request: AccountSumModel): # Get client information for this session
        accUrl = ENDPOINT + r'/apiCustomer/account/accountSummary' 
        requestDict = jsonable_encoder(request)
        accres = post(url=accUrl, json=requestDict)
        if accres.ok:
            return accres.json()

