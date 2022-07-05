from encodings import utf_8
from statistics import mode
from tokenize import String
import traceback;
import logging
from fastapi.encoders import jsonable_encoder;
from fastapi import HTTPException, status;
from urllib import request;
from http.client import HTTPException;
from requests import get,post;
from dotenv import load_dotenv;
from os import environ;

load_dotenv();
ENDPOINT = environ['SP_END_POINT']
LOG_FILENAME = environ["LOG_FILENAME"]

class CommonHelper:
        logging.basicConfig(filename=LOG_FILENAME, filemode='a', level=logging.WARN, encoding='utf-8', format='%(asctime)s - %(levelname)s - %(message)s')

        def __init__(self):
                pass
        
        @staticmethod
        def postUrl(requestUrl: String, params : request):
                requestDict = jsonable_encoder(params)
                try:
                        res = post(url= ENDPOINT + requestUrl, json=requestDict)
                        return res.json() if (res.ok) else HTTPException(status_code=res.status_code, detail=res.reason)
                except:
                        logging.error(traceback.print_exc())
                        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="INTERNAL SERVER ERROR")
