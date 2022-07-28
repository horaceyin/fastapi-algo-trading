from schemas.order_api_schemas import AddOrder, ChangeOrder, AccessOrder # Possibly unnecessary
from core.config import SP_HOST_AND_PORT
from core.endpoints import ADDORDER, CHANGEORDER, DELETEORDER, ACTIVEORDER, INACTIVEORDER
from common.common_helper import CommonHelper
import requests

# Access info from .env
ENDPOINT = SP_HOST_AND_PORT

class SPAPIHandler(): # Object to handle actions # e.g. create market order inside SPtrader, broker give parameter to handler object
    def __init__(self):
        # Login information
        # self.__accNo = "" # CONSISTENT ACROSS THE FUNCTIONS
        # self.__sessionToken = ""# CONSISTENT ACROSS THE FUNCTIONS
        pass # Not required, all variables to be used will be placed in below fucntions

    # Variables from backtesting.Broker
    def createMarketOrder(self, action, instrument, quantity, onClose: bool):
        addUrl = ENDPOINT + ADDORDER # Need to activate order to allow system to accept it
        print("Market order is being processed to SP")
        buySell = ""
        openClose = ""
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
                "accNo": "", # str # NEED TO FILL
                "buySell": buySell, # Literal["B", "S"] # B, S
                "condType": 0, # Literal[0, 1, 3, 4, 6, 8, 9] # 0 (None), 1 (Stop), 3, 4 (OCO stop), 6 (Trail stop), 8, 9 # Should be 1 if 
                "orderType": 6, # Literal[0, 2, 5, 6] # 0 (Limit), 2, 5, 6 (Market order)
                "priceInDec": "", # float # Order Not Supported if orderType is 6 # Later, need live market price from server
                "prodCode": instrument,
                "qty": quantity,
                "sessionToken": "", # str # NEED TO FILL
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
            raise SystemExit("Failed to access SP system")
        # pass # Replace with code to access SP backtesting 


    def createLimitOrder(self, action, instrument, limitPrice, quantity):
        addUrl = ENDPOINT + ADDORDER # Need to activate order to allow system to accept it
        print("Limit order is being processed to SP")
        buySell = ""
        openClose = ""
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
        try:
            addOrder = CommonHelper.post_url(addUrl,
            {
                "accNo": "", # str # NEED TO FILL
                "buySell": buySell, # Literal["B", "S"] # B, S
                "condType": 0, # Literal[0, 1, 3, 4, 6, 8, 9] # 0 (None), 1 (Stop), 3, 4 (OCO stop), 6 (Trail stop), 8, 9 # Should be 1 if 
                "orderType": 0, # Literal[0, 2, 5, 6] # 0 (Limit), 2, 5, 6 (Market order)
                "priceInDec": limitPrice, # float
                "prodCode": instrument,
                "qty": quantity,
                "sessionToken": "", # str # NEED TO FILL
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
                print("Limit order is added to SP")
            else:
                print("Limit order cannot be added to SP")
        except:
            raise SystemExit("Failed to access SP system")
    
    def createStopOrder(self, action, instrument, stopPrice, quantity):
        addUrl = ENDPOINT + ADDORDER # Need to activate order to allow system to accept it
        print("Stop order is being processed to SP")
        buySell = ""
        openClose = ""
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
        try:
            addOrder = CommonHelper.post_url(addUrl,
            {
                "accNo": "", # str # NEED TO FILL
                "buySell": buySell, # Literal["B", "S"] # B, S
                "condType": 1, # Literal[0, 1, 3, 4, 6, 8, 9] # 0 (None), 1 (Stop), 3, 4 (OCO stop), 6 (Trail stop), 8, 9 # Should be 1 if 
                "orderType": 6, # Literal[0, 2, 5, 6] # 0 (Limit), 2, 5, 6 (Market order)
                "priceInDec": "", # float # Order Not Supported if orderType is 6 # Later, need live market price from server
                "prodCode": instrument,
                "qty": quantity,
                "sessionToken": "", # str # NEED TO FILL
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
                "stopPriceInDec": stopPrice, # Optional[int]
                "stopType": "L", # Optional[Literal["L", "U", "D"]] # L (Stop loss), U (Up trigger), D (Down trigger), or blank (N/A) # Can ignore U and D
                "subCondType": 1 # Optional[Literal[0, 1, 3, 4, 6, 11, 14, 16]] # 0 (None), 1 (Stop), 3, 4 (OCO stop), 6 (Trail stop), 11 (Stop loss by price), 14 (OCO by price), 16 (Trailing stop by price)
                # upLevelInDec: Optional[float]
                # upPriceInDec: Optional[float]
                # validDate: Optional[int] # YYYYMMDD
            })
            # addOrder = CommonHelper.post_url(addUrl, request) # Access SP
            # assert addOrder["result_msg"] == "No Error"
            if addOrder["result_msg"] == "No Error":
                print("Stop order is added to SP")
            else:
                print("Stop order cannot be added to SP")
        except:
            raise SystemExit("Failed to access SP system")
        # pass # Replace with code to access SP backtesting
    
    def createStopLimitOrder(self, action, instrument, stopPrice, limitPrice, quantity):
        addUrl = ENDPOINT + ADDORDER # Need to activate order to allow system to accept it
        print("Stop limit order is being processed to SP")
        buySell = ""
        openClose = ""
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
        try:
            addOrder = CommonHelper.post_url(addUrl,
            {
                "accNo": "", # str # NEED TO FILL
                "buySell": buySell, # Literal["B", "S"] # B, S
                "condType": 1, # Literal[0, 1, 3, 4, 6, 8, 9] # 0 (None), 1 (Stop), 3, 4 (OCO stop), 6 (Trail stop), 8, 9 # Should be 1 if 
                "orderType": 0, # Literal[0, 2, 5, 6] # 0 (Limit), 2, 5, 6 (Market order)
                "priceInDec": limitPrice, # float
                "prodCode": instrument,
                "qty": quantity,
                "sessionToken": "", # str # NEED TO FILL 
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
                "stopPriceInDec": stopPrice, # Optional[int]
                "stopType": "L", # Optional[Literal["L", "U", "D"]] # L (Stop loss), U (Up trigger), D (Down trigger), or blank (N/A) # Can ignore U and D
                "subCondType": 1 # Optional[Literal[0, 1, 3, 4, 6, 11, 14, 16]] # 0 (None), 1 (Stop), 3, 4 (OCO stop), 6 (Trail stop), 11 (Stop loss by price), 14 (OCO by price), 16 (Trailing stop by price)
                # upLevelInDec: Optional[float]
                # upPriceInDec: Optional[float]
                # validDate: Optional[int] # YYYYMMDD
            })
            # addOrder = CommonHelper.post_url(addUrl, request) # Access SP
            # assert addOrder["result_msg"] == "No Error"
            if addOrder["result_msg"] == "No Error":
                print("Stop limit order is added to SP")
            else:
                print("Stop limit order cannot be added to SP")
        except:
            raise SystemExit("Failed to access SP system")
        # pass # Replace with code to access SP backtesting

    def activeOrder(self, accOrderNo, action, instrument):
        activeUrl = ENDPOINT + ACTIVEORDER
        print("Activation of order is being processed in SP")
        buySell = ""
        if action == 1 or action == 2:
            buySell = "B"
        elif action == 3 or action == 4:
            buySell = "S"
        try:
            activeOrder = CommonHelper.post_url(activeUrl,
            {
                "accNo": "", # str
                "accOrderNo": accOrderNo, # int
                "buySell": buySell, # Literal["B", "S"] # B, S
                "prodCode": instrument,
                "sessionToken": "", # str
                "extOrderId": 0, # Literal[0, 1, 2, 3, 4] = 0 # 0 - 4 # Unsure of purpose
            })
            # activeOrder = CommonHelper.post_url(activeUrl, request) # Access SP
            if activeOrder["result_msg"] == "No Error":
                print("Order is activated in SP")
            elif activeOrder["result_msg"] == "Order Is Already Active":
                print("Order is already active in SP")
            else:
                print("Order cannot be activated in SP")
        except:
            raise SystemExit("Failed to access SP system")

    def inactiveOrder(self, accOrderNo, action, instrument):
        inactiveUrl = ENDPOINT + INACTIVEORDER
        print("Deactivation of order is being processed in SP")
        buySell = ""
        if action == 1 or action == 2:
            buySell = "B"
        elif action == 3 or action == 4:
            buySell = "S"
        try:
            inactiveOrder = CommonHelper.post_url(inactiveUrl,
            {
                "accNo": "", # str
                "accOrderNo": accOrderNo, # int
                "buySell": buySell, # Literal["B", "S"] # B, S
                "prodCode": instrument,
                "sessionToken": "", # str
                "extOrderId": 0, # Literal[0, 1, 2, 3, 4] = 0 # 0 - 4 # Unsure of purpose
            })
            # inactiveOrder = CommonHelper.post_url(inactiveUrl, request) # Access SP
            if inactiveOrder["result_msg"] == "No Error":
                print("Order is deactivated in SP")
            elif inactiveOrder["result_msg"] == "Order Is Already Inactive":
                print("Order is already inactive")
            else:
                print("Order cannot be deactivated in SP")
        except:
            raise SystemExit("Failed to access SP system")

    def changeOrder(self, accOrderNo, buySell, instrument, price, quantity, stopPrice): # price, quantity, stopPrice should be optional; stopPrice will cause function to fail if order is not stop or stopLimit
        changeUrl = ENDPOINT + CHANGEORDER
        print("SP is changing order properties")
        try:
            changeOrder = CommonHelper.post_url(changeUrl,
            {
                "accNo": "", # str
                "accOrderNo": accOrderNo, # int
                "buySell": buySell, # Literal["B", "S"] # B, S
                "prodCode": instrument,
                "sessionToken": "", # str
                # downLevelInDec: Optional[float]
                # downPriceInDec: Optional[float]
                "extOrderId": 0, # Literal[0, 1, 2, 3, 4] = 0 # 0 - 4 # Unsure of purpose
                "priceInDec": price, # Optional[float]
                "qty": quantity, # Optional[int]
                # schedTime: Optional[float] # In the form YYYYMMDD.hhmmss # Unsure of formatting
                "stopPriceInDec": stopPrice, # Optional[float]
                # upLevelInDec: Optional[float]
                # upPriceInDec: Optional[float]
                # validDate: Optional[int] # YYYYMMDD
            })
            # changeOrder = CommonHelper.post_url(changeUrl, request) # Access SP
            # assert changeOrder["result_msg"] == "No Error"
            if changeOrder["result_msg"] == "No Error":
                print("SP has changed order properties")
            else:
                print("SP cannot change order properties")
        except:
            raise SystemExit("Failed to access SP system")

    def cancelOrder(self, accOrderNo, action, instrument):
        deleteUrl = ENDPOINT + DELETEORDER
        print("Deletion of order is being processed to SP")
        buySell = ""
        if action == 1 or action == 2:
            buySell = "B"
        elif action == 3 or action == 4:
            buySell = "S"
        try:
            deleteOrder = CommonHelper.post_url(deleteUrl,
            {
                "accNo": "", # str
                "accOrderNo": accOrderNo, # int
                "buySell": buySell, # Literal["B", "S"] # B, S
                "prodCode": instrument,
                "sessionToken": "", # str
                "extOrderId": 0, # Literal[0, 1, 2, 3, 4] = 0 # 0 - 4 # Unsure of purpose
            })
            # deleteOrder = CommonHelper.post_url(deleteUrl, request) # Access SP
            # assert deleteOrder["result_msg"] == "No Error"
            if deleteOrder["result_msg"] == "No Error":
                print("Order is deleted from SP")
            else:
                print("Order cannot be deleted from SP")
        except:
            raise SystemExit("Failed to access SP system")

# test = SPAPIHandler()
# test.createMarketOrder(1, 'HSIN2', 1, False)