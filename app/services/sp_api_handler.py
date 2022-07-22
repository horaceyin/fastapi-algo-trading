from app.core.endpoints import ACTIVEORDER
from app.schemas.order_api_schemas import AddOrder, ChangeOrder, AccessOrder
from core.config import SP_HOST_AND_PORT
from core.endpoints import ADDORDER, CHANGEORDER, DELETEORDER, ACTIVEORDER, INACTIVEORDER
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
    def createMarketOrder(self, request: AddOrder):
        addUrl = ENDPOINT + ADDORDER # Need to activate order to allow system to accept it
        print("Market order is being processed to SP")
        try:
            addOrder = CommonHelper.post_url(addUrl, request)
            # assert addOrder["result_msg"] == "No Error"
            if addOrder["result_msg"] == "No Error":
                print("Market order is added to SP")
            else:
                print("Market order cannot be added to SP")
        except:
            raise SystemExit("Market order cannot be added to SP")
        # pass # Replace with code to access SP backtesting 

    def createLimitOrder(self, request: AddOrder):
        addUrl = ENDPOINT + ADDORDER # Need to activate order to allow system to accept it
        print("Limit order is being processed to SP")
        try:
            addOrder = CommonHelper.post_url(addUrl, request)
            # assert addOrder["result_msg"] == "No Error"
            if addOrder["result_msg"] == "No Error":
                print("Limit order is added to SP")
            else:
                print("Limit order cannot be added to SP")
        except:
            raise SystemExit("Limit order cannot be added to SP")
        # pass # Replace with code to access SP backtesting
    
    def createStopOrder(self, request: AddOrder):
        addUrl = ENDPOINT + ADDORDER # Need to activate order to allow system to accept it
        print("Stop order is being processed to SP")
        try:
            addOrder = CommonHelper.post_url(addUrl, request)
            # assert addOrder["result_msg"] == "No Error"
            if addOrder["result_msg"] == "No Error":
                print("Stop order is added to SP")
            else:
                print("Stop order cannot be added to SP")
        except:
            raise SystemExit("Stop order cannot be added to SP")
        # pass # Replace with code to access SP backtesting
    
    def createStopLimitOrder(self, request: AddOrder):
        addUrl = ENDPOINT + ADDORDER # Need to activate order to allow system to accept it
        print("Stop limit order is being processed to SP")
        try:
            addOrder = CommonHelper.post_url(addUrl, request)
            # assert addOrder["result_msg"] == "No Error"
            if addOrder["result_msg"] == "No Error":
                print("Stop limit order is added to SP")
            else:
                print("Stop limit order cannot be added to SP")
        except:
            raise SystemExit("Stop limit order cannot be added to SP")
        # pass # Replace with code to access SP backtesting

    def activeOrder(self, request: AccessOrder):
        activeUrl = ENDPOINT + ACTIVEORDER
        print("Activation of order is being processed in SP")
        try:
            activeOrder = CommonHelper.post_url(activeUrl, request)
            if activeOrder["result_msg"] == "No Error":
                print("Order is activated in SP")
            elif activeOrder["result_msg"] == "Order Is Already Active":
                print("Order is already active in SP")
            else:
                print("Order cannot be activated in SP")
        except:
            raise SystemExit("Order cannot be activated in SP")

    def inactiveOrder(self, request: AccessOrder):
        inactiveUrl = ENDPOINT + INACTIVEORDER
        print("Deactivation of order is being processed in SP")
        try:
            inactiveOrder = CommonHelper.post_url(inactiveUrl, request)
            if inactiveOrder["result_msg"] == "No Error":
                print("Order is deactivated in SP")
            elif inactiveOrder["result_msg"] == "Order Is Already Inactive":
                print("Order is already inactive")
            else:
                print("Order cannot be deactivated in SP")
        except:
            raise SystemExit("Order cannot be deactivated in SP")

    def changeOrder(self, request: ChangeOrder):
        changeUrl = ENDPOINT + CHANGEORDER
        print("SP is changing order properties")
        try:
            changeOrder = CommonHelper.post_url(changeUrl, request)
            # assert changeOrder["result_msg"] == "No Error"
            if changeOrder["result_msg"] == "No Error":
                print("SP has changed order properties")
            else:
                print("SP cannot change order properties")
        except:
            raise SystemExit("SP cannot change order properties")

    def cancelOrder(self, request: AccessOrder):
        deleteUrl = ENDPOINT + DELETEORDER
        print("Deletion of order is being processed to SP")
        try:
            deleteOrder = CommonHelper.post_url(deleteUrl, request)
            # assert deleteOrder["result_msg"] == "No Error"
            if deleteOrder["result_msg"] == "No Error":
                print("Order is deleted from SP")
            else:
                print("Order cannot be deleted from SP")
        except:
            raise SystemExit("Order cannot be deleted from SP")