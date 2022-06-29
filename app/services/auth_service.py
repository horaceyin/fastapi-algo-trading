import json
from os import environ
import traceback
from dotenv import load_dotenv
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from requests import get, post
from schemas.auth_schemas import UserLogin
from common.common_helper import CommonHelper

load_dotenv()
ENDPOINT = environ['SP_END_POINT']
LOG_FILENAME = environ["LOG_FILENAME"]

class AuthService:
    def __init__(self):
        pass

    @staticmethod
    def user_login(request: UserLogin):
        myUrl = ENDPOINT + "/apiCustomer/accessRight/userLogin"
        return CommonHelper.postUrl(requestUrl=myUrl, params=request);
        
        
        # requestDict = jsonable_encoder(request)
        # try:
        #     res = post(url=myUrl, json=requestDict)
        #     return (res.ok) if res.json() else HTTPException(status_code=res.status_code, detail=res.reason)
        # except:
        #     traceback.print_exc(file=LOG_FILENAME)
        #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="INTERNAL SERVER ERROR")
