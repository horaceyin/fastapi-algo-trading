import logging
import traceback
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException, status, Request
from requests import get, post
from core.config import ENV_FILE, SP_HOST_AND_PORT

ENDPOINT = SP_HOST_AND_PORT
LOG_PATH = ENV_FILE["LOG_PATH"]

# doing common requests.post() method

class CommonHelper:
        logging.basicConfig(filename=LOG_PATH, filemode='a', level=logging.WARN, encoding='utf-8', format='%(asctime)s - %(levelname)s - %(message)s')
        def __init__(self):
                pass
        
        @staticmethod
        def post_url(requestUrl: str, params: Request):
                requestDict = jsonable_encoder(params)
                try:
                        # Make post request
                        res = post(url=requestUrl, json=requestDict) 
                        # Return text/JSON response if any, so long as status code < 400, otherwise give error
                        if res.ok:
                                try: return res.json()
                                except: return res.text
                        else:
                               HTTPException(status_code=res.status_code, detail=res.reason)
                except: 
                        logging.error(traceback.print_exc())
                        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="INTERNAL SERVER ERROR")

        @staticmethod
        def get_url(request_url):
                try:
                        res = get(url=request_url)
                        if res.ok:
                                try: return res.json()
                                except: return res.text
                        else:
                                HTTPException(status_code=res.status_code, detail=res.reason)
                except:
                        logging.error(traceback.print_exc())
                        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="INTERNAL SERVER ERROR")