import json

from requests import request
from core.endpoints import ACTIVEORDER
from schemas.order_api_schemas import AddOrder, ChangeOrder, AccessOrder # Possibly unnecessary
from core.config import SP_HOST_AND_PORT
from core.endpoints import ADDORDER, CHANGEORDER, DELETEORDER, ACTIVEORDER, INACTIVEORDER
from common.common_helper import CommonHelper
import requests

# Access info from .env
ENDPOINT = SP_HOST_AND_PORT

class Test: # Object to handle actions # e.g. create market order inside SPtrader, broker give parameter to handler object
    # def __init__(self, instrument, quantity, onClose):
    def __init__(self):
        # Login information
        pass # Not required, all variables to be used will be placed in below fucntions

    # Variables from backtesting.Broker
    def createMarketOrder(self, action, instrument, quantity, onClose):
        addUrl = ENDPOINT + ADDORDER # Need to activate order to allow system to accept it
        print("Market order is being processed to SP")
        if action == 1:
            buySell = "B"
            openClose = "O"
        elif action == 2:
            buySell = "B"
            openClose = "C"
        elif action == 3:
            buySell = "S"
            openClose = "C"
        elif action == 4:
            buySell = "S"
            openClose = "O"
        if onClose is True and (action == 2 or action == 3):
            openClose = "M"
        try:
            addOrder = CommonHelper.post_url(addUrl,
            {
                "accNo": "ANSONLI01", # str # NEED TO FILL
                "buySell": buySell, # Literal["B", "S"] # B, S
                "condType": 0, # Literal[0, 1, 3, 4, 6, 8, 9] # 0 (None), 1 (Stop), 3, 4 (OCO stop), 6 (Trail stop), 8, 9 # Should be 1 if 
                "orderType": 0, # Literal[0, 2, 5, 6] # 0 (Limit), 2, 5, 6 (Market order) #orderType 6 is only working for real trading but not simulated trading
                "priceInDec": "20700.0", # float
                "prodCode": instrument,
                "qty": quantity,
                "sessionToken": "201ca50220ea12a73d917cbeeecc02cf", # str # NEED TO FILL
                "validType": 0, # Literal[0, 1, 2, 3, 4] = 0 # 0 - 4 # Unsure of purpose
                # "clOrderId": Optional[str] 
                # downLevelInDec: Optional[float]
                # downPriceInDec: Optional[float]
                "openClose": openClose, # Optional[Literal["M", "O", "C"]] # M (Mandatory close), O (Open), C (Close)
                "options": 0, 
                # ref: Optional[str]
                # ref2: Optional[str]
                # schedTime: Optional[float] # In the form YYYYMMDD.hhmmss # Unsure of formatting
                "status": 0, # Optional[Literal[2]] # Only required in inactive orders (2 = Inactive)
                "stopPriceInDec": 0, # Optional[int]
                "stopType": "", # Optional[Literal["L", "U", "D"]] # L (Stop loss), U (Up trigger), D (Down trigger), or blank (N/A) # Can ignore U and D
                "subCondType": 0 # Optional[Literal[0, 1, 3, 4, 6, 11, 14, 16]] # 0 (None), 1 (Stop), 3, 4 (OCO stop), 6 (Trail stop), 11 (Stop loss by price), 14 (OCO by price), 16 (Trailing stop by price)
                # upLevelInDec: Optional[float]
                # upPriceInDec: Optional[float]
                # validDate: Optional[int] # YYYYMMDD
            })
            # addOrder = CommonHelper.post_url(addUrl, request1) # Access SP
            # assert addOrder["result_msg"] == "No Error"
            if addOrder["result_msg"] == "No Error":
                print("Market order is added to SP")
            else:
                print(addOrder)
                print(addOrder["result_msg"])
        except:
            raise SystemExit("Market order cannot be added to SP")
        # pass # Replace with code to access SP backtesting 
test = Test()
test.createMarketOrder(4,'HSIU2',1,False)
