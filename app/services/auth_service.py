import json
from os import environ
from dotenv import load_dotenv
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from requests import get, post
from schemas.auth_schemas import UserLogin, UserInfo

load_dotenv()
ENDPOINT = environ['SP_END_POINT']

class AuthService:
    def __init__(self):
        pass

    @staticmethod
    def user_login(request: UserLogin):
        myUrl = ENDPOINT + r'/apiCustomer/accessRight/userLogin'
        requestDict = jsonable_encoder(request)
        res = post(url=myUrl, json=requestDict)
        if res.ok:
            return res.json()
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT, detail="Request Timeout with SP Server.")
    
    def user_info(request: UserInfo):
        infoUrl = ENDPOINT + r'/apiCustomer/account/accountSummary'
        requestDict = jsonable_encoder(request)
        res = post(url = infoUrl, json = requestDict)
        if res.ok:
            return res.json()
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT, detail="Request Timeout with SP Server.")
    