

import traceback
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException, status
from urllib import request
from requests import get, post
from dotenv import load_dotenv
from os import environ

load_dotenv()
ENDPOINT = environ['SP_END_POINT']
LOG_FILENAME = environ["LOG_FILENAME"]

class CommonHelper:
        def __init__(self):
                pass
        
        @staticmethod
        def post_url(requestUrl: str, params: request):
                print(type(params))
                requestDict = jsonable_encoder(params)
                try:
                        res = post(url=requestUrl, json=requestDict)
                        return res.json() if (res.ok) else HTTPException(status_code=res.status_code, detail=res.reason)
                except:
                        traceback.print_exc(file=LOG_FILENAME)
                        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="INTERNAL SERVER ERROR")
