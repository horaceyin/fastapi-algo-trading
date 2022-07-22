from app.core.endpoints import ACTIVEORDER
from app.schemas.order_api_schemas import AddOrder, DeleteOrder
from core.config import SP_HOST_AND_PORT
from core.endpoints import ADDORDER, CHANGEORDER, DELETEORDER
import requests
import json
from schemas.technical_analysis_schemas import GetDoneTradeModel
from common.common_helper import CommonHelper
from app.services.technical_analysis_service import PnLService

# Access info from .env
ENDPOINT = SP_HOST_AND_PORT

class SPAPIHandler(): # Object to handle actions # e.g. create market order inside SPtrader, broker give parameter to handler object
    def __init__(self):
        # Login information
        pass # Not required, all variables to be used will be placed in below fucntions

    # Variables from backtesting.Broker
    def createMarketOrder(self, request: AddOrder, action, instrument, quantity, onClose=False):
        addUrl = ENDPOINT + ADDORDER # Need to activate order to allow system to accept it
        activeUrl = ENDPOINT + ACTIVEORDER
        print("Market order is being processed")
        try:
            addOrder = CommonHelper.post_url(addUrl, request)
            if addOrder["result_msg"] == "No Error":
                print("Market order is added")
            else:
                raise SystemExit("Market order cannot be added")
        except:
            raise SystemExit("Market order cannot be added")
        # pass # Replace with code to access SP backtesting 

    def createLimitOrder(self, request: AddOrder, action, instrument, limitPrice, quantity):
        addUrl = ENDPOINT + ADDORDER # Need to activate order to allow system to accept it
        activeUrl = ENDPOINT + ACTIVEORDER
        print("Limit order is being processed")
        try:
            addOrder = CommonHelper.post_url(addUrl, request)
            if addOrder["result_msg"] == "No Error":
                print("Limit order is added")
            else:
                raise SystemExit("Limit order cannot be added")
        except:
            raise SystemExit("Limit order cannot be added")
        # pass # Replace with code to access SP backtesting
    
    def createStopOrder(self, request: AddOrder, action, instrument, stopPrice, quantity):
        addUrl = ENDPOINT + ADDORDER # Need to activate order to allow system to accept it
        activeUrl = ENDPOINT + ACTIVEORDER
        print("Stop order is being processed")
        try:
            addOrder = CommonHelper.post_url(addUrl, request)
            if addOrder["result_msg"] == "No Error":
                print("Stop order is added")
            else:
                raise SystemExit("Stop order cannot be added")
            print("Stop order is added")
        except:
            raise SystemExit("Stop order cannot be added")
        # pass # Replace with code to access SP backtesting
    
    def createStopLimitOrder(self, request: AddOrder, action, instrument, stopPrice, limitPrice, quantity):
        addUrl = ENDPOINT + ADDORDER # Need to activate order to allow system to accept it
        activeUrl = ENDPOINT + ACTIVEORDER
        print("Stop limit order is being processed")
        try:
            addOrder = CommonHelper.post_url(addUrl, request)
            if addOrder["result_msg"] == "No Error":
                print("Stop limit order is added")
            else:
                raise SystemExit("Stop limit order cannot be added")
            print("Stop limit order is added")
        except:
            raise SystemExit("Stop limit order cannot be added")
        # pass # Replace with code to access SP backtesting

    def cancelOrder(self, request: DeleteOrder, order):
        deleteUrl = ENDPOINT + DELETEORDER
        print("Deletion of order is being processed")
        try:
            deleteOrder = CommonHelper.post_url(deleteUrl, request)
            if deleteOrder["result_msg"] == "No Error":
                print("Order is deleted")
            else:
                raise SystemExit("Order cannot be deleted")
        except:
            raise SystemExit("Order cannot be deleted")