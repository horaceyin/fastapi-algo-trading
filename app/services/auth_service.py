from os import environ
from dotenv import load_dotenv
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from requests import get, post
from schemas.auth_schemas import UserLogin, AccountSumModel

load_dotenv()
ENDPOINT = environ['SP_END_POINT']

class AuthService:
    def __init__(self):
        pass


    @staticmethod # Method is instance method otherwise
    def user_login(request: UserLogin): # Get token for this session
        myUrl = ENDPOINT + r'/apiCustomer/accessRight/userLogin' 
        requestDict = jsonable_encoder(request)
        res = post(url=myUrl, json=requestDict)
        print(res, "$$$$$$$") # Testing code
        if res.ok:
            return res.json()
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT, detail="Request Timeout with SP Server.")

    @staticmethod
    def acc_login(request: AccountSumModel): # Get client information for this session
        accUrl = ENDPOINT + r'/apiCustomer/account/accountSummary' 
        requestDict = jsonable_encoder(request)
        accres = post(url=accUrl, json=requestDict)
        if accres.ok:
            return accres.json()
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT, detail="Request Timeout with SP Server.")