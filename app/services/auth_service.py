from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from requests import get, post
from schemas.auth_schemas import UserLogin

BASE_URL = r'http://192.168.123.221:9030'

class AuthService:
    def __init__(self):
        pass

    @staticmethod
    def user_login(request: UserLogin):
        myUrl = BASE_URL + r'/apiCustomer/accessRight/userLogin'
        requestDict = jsonable_encoder(request)
        res = post(url=myUrl, json=requestDict)
        if res.ok:
            return res.json()
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT, detail="Request Timeout with SP Server.")