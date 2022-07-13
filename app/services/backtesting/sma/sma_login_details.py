import requests
import json
from schemas.backtesting_schemas import BacktestingModel
from core.endpoints import PRODINFO, CCYRATES, USERLOGIN, ACCOUNTINFO
from os import environ
from dotenv import load_dotenv

# Access info from .env
load_dotenv()
ENDPOINT = environ['SP_HOST_AND_PORT']

class portSize:
    def __init__(self, userid, password, targetacc):
        self.__userid = userid
        self.__password = password
        self.__targetacc = targetacc

    def loginData(self):
        # Login
        accessurl = ENDPOINT + ACCOUNTINFO
        userid = self.__userid
        password = self.__password
        access = requests.post(accessurl, 
        json = {
            "password": password,
            "userId": userid,
            "apiAppId": "SP_F",
            "mode": 0
        })
        dataDict = json.loads(access.text) 
        token = dataDict['data']['sessionToken'] # Session token to access other requests

        accsum = ENDPOINT + ACCOUNTINFO
        targetAcc = self.__targetacc
        accResponse = requests.post(accsum,
            json = {
                "sessionToken": token,
                "targetAccNo": targetAcc
            })
        summaryDict = json.loads(accResponse.text)
        portfolio_size = summaryDict['data']['avFund']
        return portfolio_size