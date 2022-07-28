from core.endpoints import ACTIVEORDER
from schemas.order_api_schemas import AddOrder, ChangeOrder, AccessOrder
from core.config import SP_HOST_AND_PORT
from core.endpoints import ADDORDER, CHANGEORDER, DELETEORDER, ACTIVEORDER, INACTIVEORDER
from common.common_helper import CommonHelper
import requests

# Access info from .env
ENDPOINT = SP_HOST_AND_PORT

class SPAPIHandler(): # Object to handle actions # e.g. create market order inside SPtrader, broker give parameter to handler object
    def __init__(self, instrument, quantity, onClose):
        # Login information
        self.__instrument = instrument
        self.__quantity = quantity
        self.__onClose = onClose
        # pass # Not required, all variables to be used will be placed in below fucntions

    # Variables from backtesting.Broker
    def createMarketOrder(self):
        addUrl = ENDPOINT + ADDORDER # Need to activate order to allow system to accept it
        if self.__onClose is False:
            openClose = "M"
        else:
            openClose = "C" # LATER NEEDS TO BE SET SUCH THAT IT CAN CHANGE BETWEEN OPEN AND CLOSE
        print("Market order is being processed to SP")
        try:
            addOrder = requests.post(addUrl,
            json ={
                "accNo": "", # str
                "buySell": "", # Literal["B", "S"] # B, S
                "condType": 0, # Literal[0, 1, 3, 4, 6, 8, 9] # 0 (None), 1 (Stop), 3, 4 (OCO stop), 6 (Trail stop), 8, 9 # Should be 1 if 
                "orderType": 6, # Literal[0, 2, 5, 6] # 0 (Limit), 2, 5, 6 (Market order)
                "priceInDec": "", # float
                "prodCode": self.__instrument,
                "qty": self.__quantity,
                "sessionToken": "", # str
                "validType": 0, # Literal[0, 1, 2, 3, 4] = 0 # 0 - 4 # Unsure of purpose
                # "clOrderId": Optional[str] 
                # downLevelInDec: Optional[float]
                # downPriceInDec: Optional[float]
                "openClose": openClose, # Optional[Literal["M", "O", "C"]] # M (Mandatory close), O (Open), C (Close)
                # options: Optional[int] # Unsure of purpose
                # ref: Optional[str]
                # ref2: Optional[str]
                # schedTime: Optional[float] # In the form YYYYMMDD.hhmmss # Unsure of formatting
                "status": 2, # Optional[Literal[2]] # Only required in inactive orders (2 = Inactive)
                "stopPriceInDec": 0, # Optional[int]
                "stopType": "", # Optional[Literal["L", "U", "D"]] # L (Stop loss), U (Up trigger), D (Down trigger), or blank (N/A) # Can ignore U and D
                "subCondType": 0 # Optional[Literal[0, 1, 3, 4, 6, 11, 14, 16]] # 0 (None), 1 (Stop), 3, 4 (OCO stop), 6 (Trail stop), 11 (Stop loss by price), 14 (OCO by price), 16 (Trailing stop by price)
                # upLevelInDec: Optional[float]
                # upPriceInDec: Optional[float]
                # validDate: Optional[int] # YYYYMMDD
            })
            # addOrder = CommonHelper.post_url(addUrl, request) # Access SP
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
        if self.__onClose is False:
            openClose = "M"
        else:
            openClose = "C" # LATER NEEDS TO BE SET SUCH THAT IT CAN CHANGE BETWEEN OPEN AND CLOSE
        print("Limit order is being processed to SP")
        try:
            addOrder = requests.post(addUrl,
            json ={
                "accNo": "", # str
                "buySell": "", # Literal["B", "S"] # B, S
                "condType": 0, # Literal[0, 1, 3, 4, 6, 8, 9] # 0 (None), 1 (Stop), 3, 4 (OCO stop), 6 (Trail stop), 8, 9 # Should be 1 if 
                "orderType": 6, # Literal[0, 2, 5, 6] # 0 (Limit), 2, 5, 6 (Market order)
                "priceInDec": "", # float
                "prodCode": self.__instrument,
                "qty": self.__quantity,
                "sessionToken": "", # str
                "validType": 0, # Literal[0, 1, 2, 3, 4] = 0 # 0 - 4 # Unsure of purpose
                # "clOrderId": Optional[str] 
                # downLevelInDec: Optional[float]
                # downPriceInDec: Optional[float]
                "openClose": openClose, # Optional[Literal["M", "O", "C"]] # M (Mandatory close), O (Open), C (Close)
                # options: Optional[int] # Unsure of purpose
                # ref: Optional[str]
                # ref2: Optional[str]
                # schedTime: Optional[float] # In the form YYYYMMDD.hhmmss # Unsure of formatting
                "status": 2, # Optional[Literal[2]] # Only required in inactive orders (2 = Inactive)
                "stopPriceInDec": 0, # Optional[int]
                "stopType": "", # Optional[Literal["L", "U", "D"]] # L (Stop loss), U (Up trigger), D (Down trigger), or blank (N/A) # Can ignore U and D
                "subCondType": 0 # Optional[Literal[0, 1, 3, 4, 6, 11, 14, 16]] # 0 (None), 1 (Stop), 3, 4 (OCO stop), 6 (Trail stop), 11 (Stop loss by price), 14 (OCO by price), 16 (Trailing stop by price)
                # upLevelInDec: Optional[float]
                # upPriceInDec: Optional[float]
                # validDate: Optional[int] # YYYYMMDD
            })
            # addOrder = CommonHelper.post_url(addUrl, request) # Access SP
            # addOrder = CommonHelper.post_url(addUrl, request) # Access SP
            # assert addOrder["result_msg"] == "No Error"
            if addOrder["result_msg"] == "No Error":
                print("Limit order is added to SP")
            else:
                print("Limit order cannot be added to SP")
        except:
            raise SystemExit("Limit order cannot be added to SP")
    
    def createStopOrder(self, request: AddOrder):
        addUrl = ENDPOINT + ADDORDER # Need to activate order to allow system to accept it
        print("Stop order is being processed to SP")
        try:
            addOrder = CommonHelper.post_url(addUrl, request) # Access SP
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
            addOrder = CommonHelper.post_url(addUrl, request) # Access SP
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
            activeOrder = CommonHelper.post_url(activeUrl, request) # Access SP
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
            inactiveOrder = CommonHelper.post_url(inactiveUrl, request) # Access SP
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
            changeOrder = CommonHelper.post_url(changeUrl, request) # Access SP
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
            deleteOrder = CommonHelper.post_url(deleteUrl, request) # Access SP
            # assert deleteOrder["result_msg"] == "No Error"
            if deleteOrder["result_msg"] == "No Error":
                print("Order is deleted from SP")
            else:
                print("Order cannot be deleted from SP")
        except:
            raise SystemExit("Order cannot be deleted from SP")
     
    # def makeFuture(self, request: MakeFuture):
    #     makeTargUrl = ENDPOINT + MAKEPOSITION
    #     print("Future position is being processed to SP")
    #     try:
    #         makeTarget = CommonHelper.post_url(makeTargUrl, request) # Access SP
    #         # assert deleteOrder["result_msg"] == "No Error"
    #         if makeTarget["result_msg"] == "No Error":
    #             print("Future position is made in SP")
    #         else:
    #             print("Future position cannot be made in SP")
    #     except:
    #         raise SystemExit("Future position cannot be made in SP")