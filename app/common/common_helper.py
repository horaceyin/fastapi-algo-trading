import logging
import traceback
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException, status, Request
from requests import get, post
from dotenv import load_dotenv
from os import environ

load_dotenv()
ENDPOINT = environ['SP_HOST_AND_PORT']
LOG_FILENAME = environ["LOG_FILENAME"]

class CommonHelper:
        logging.basicConfig(filename=LOG_FILENAME, filemode='a', level=logging.WARN, encoding='utf-8', format='%(asctime)s - %(levelname)s - %(message)s')
        def __init__(self):
                pass
        
        @staticmethod
        def post_url(requestUrl: str, params: Request):
                requestDict = jsonable_encoder(params)
                try:
                        res = post(url=requestUrl, json=requestDict)
                        return res.json() if (res.ok) else HTTPException(status_code=res.status_code, detail=res.reason)
                except:
                        logging.error(traceback.print_exc())
                        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="INTERNAL SERVER ERROR")
