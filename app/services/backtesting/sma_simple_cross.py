from pyalgotrade import strategy
from pyalgotrade.technical import ma
from pyalgotrade.technical import cross

# from pyalgotrade.stratanalyzer import returns
# retAnalyzer = returns.Returns()

import requests
import json
import datetime

from iteration_utilities import unique_everseen # Remove duplicates in lists

from os import environ
from dotenv import load_dotenv

from core.endpoints import ADMININFO, PRODINFO, CCYRATES

# Access info from .env
load_dotenv()
ENDPOINT = environ['SP_HOST_AND_PORT']
LOG_FILENAME = environ["LOG_FILENAME"]

class SMACrossOver(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, smaPeriod):
        super(SMACrossOver, self).__init__(feed)
        self.__instrument = instrument
        self.__position = None
        # We'll use adjusted close values instead of regular close values.
        #self.setUseAdjustedValues(True)
        self.__prices = feed[instrument].getPriceDataSeries()
        self.__sma = ma.SMA(self.__prices, smaPeriod)
        self.__time = 0

    def get_sma(self):
        global access, token2, alltrades, buymoments, sellmoments
        accessurl = ENDPOINT + ADMININFO
        access = requests.post(accessurl, 
        json = {
            "password": "sp",
            "userId": "SPNICHOLAS",
            "apiAppId": "SP_F",
            "mode": 0
        })
        dataDict = json.loads(access.text) 
        token2 = dataDict['data']['sessionToken'] # Session token to access other requests
        # To transfer dictionary object to below
        alltrades = []

        # Sort moments below by date, then by time
        buymoments = [] # Make list of dictionaries for buying moments # Need to find way to get date and time
        buymoments.sort(key = lambda x: datetime.strptime(x['Date'], '%Y-%m-%d'))
        buymoments.sort(key = lambda x: datetime.strptime(x['Time'], '%H-%M-%S'))
        
        sellmoments =[] # Make list of dictionaries for selling moments # Need to find way to get date and time
        sellmoments.sort(key = lambda x: datetime.strptime(x['Date'], '%Y-%m-%d'))
        sellmoments.sort(key = lambda x: datetime.strptime(x['Time'], '%H-%M-%S'))
        return self.__sma # <pyalgotrade.technical.ma.SMA object at 0x11c0644c0>

    def on_start(self):
        # def boundary_input(): # Define boundary value
        #     global boundaryValue
        #     while True:
        #         try:
        #             boundaryValue = float(input("Enter the boundary value: "))
        #         except ValueError:
        #             print("Invalid. Try again: ")
        #             continue
        #         else:
        #             break
        # boundary_input()
        print ("Initial portfolio value: $%.2f" % self.getBroker().getCash()) # Gives initial portfolio value

    def on_enter_ok(self, position):
        global recordval1
        execInfo = position.getEntryOrder().getExecutionInfo()
        produrl = ENDPOINT + PRODINFO
        productinfo = requests.post(produrl, 
        json = {
            "prodCode": self.__instrument, # Collects product code from sma_cross2, which collects from sma_strat2
            "sessionToken": token2,
            "dataRecordTotal": 100,
            "dataStartFromRecord": 0
        })
        recordDiction = json.loads(productinfo.text) 
        if recordDiction['result_code'] == 40011:
            recordsize = 0
            recordccy = "HKD"
        else:
            recordsize = recordDiction['data']['jsonData']['contractSize'] # Size of product
            recordccy = recordDiction['data']['jsonData']['ccy'] # Currency of product

        ccyrate = ENDPOINT + CCYRATES
        ccyratein = requests.post(ccyrate, 
        json = {
            "ccy": recordccy, # USD = 1
            "sessionToken": token2
        })
        ccyrateintext = json.loads(ccyratein.text) 
        if ccyrateintext['result_code'] == 40011:
            ccyrateinval = 1 
        else: 
            ccyrateinval = ccyrateintext['data']['recordData'][0]['rate'] # USD to recordccy
        ccyrateout = requests.post(ccyrate, 
        json = {
            "ccy": "HKD", 
            "sessionToken": token2
        })
        ccyrateouttext = json.loads(ccyrateout.text) 
        if ccyrateouttext['result_code'] == 40011:
            ccyrateoutval = 1 
        else: 
            ccyrateoutval = ccyrateouttext['data']['recordData'][0]['rate'] # USD to HKD
        recordval1 = recordsize * execInfo.getPrice() * ccyrateoutval/ccyrateinval # Contract size multipled by number of points
        
        self.info("BUY at $%.2f" % (recordval1)) # Actual price
        # self.info("BUY at $%.2f" % (execInfo.getPrice())) # In terms of points
        currenttime = self.getCurrentDateTime()
        newinfo = {
                "Date": currenttime.date().strftime('%Y-%m-%d'), 
                "Time": currenttime.time().strftime('%H:%M:%S'), 
                "Action": "BUY", 
                "Price": recordval1
            }
        buymoments.append(newinfo)
        self.__time = self.__time + 1
        print ("New portfolio value: $%.2f" % self.getBroker().getCash())
        print(self.__time)

    def on_enter_canceled(self, position):
        self.__position = None
    
    def on_exit_ok(self, position):
        execInfo = position.getExitOrder().getExecutionInfo()
        produrl = ENDPOINT + PRODINFO
        productinfo = requests.post(produrl, 
        json = {
            "prodCode": self.__instrument, # Collects product code from sma_cross2, which collects from sma_strat2
            "sessionToken": token2,
            "dataRecordTotal": 100,
            "dataStartFromRecord": 0
        })
        recordDiction = json.loads(productinfo.text) 
        if recordDiction['result_code'] == 40011:
            recordsize = 0
            recordccy = "HKD"
        else:
            recordsize = recordDiction['data']['jsonData']['contractSize'] # Size of product
            recordccy = recordDiction['data']['jsonData']['ccy'] # Currency of product

        ccyrate = ENDPOINT + CCYRATES
        ccyratein = requests.post(ccyrate, 
        json = {
            "ccy": recordccy, # USD = 1
            "sessionToken": token2
        })
        ccyrateintext = json.loads(ccyratein.text) 
        if ccyrateintext['result_code'] == 40011:
            ccyrateinval = 1 
        else: 
            ccyrateinval = ccyrateintext['data']['recordData'][0]['rate'] # USD to recordccy
        ccyrateout = requests.post(ccyrate, 
        json = {
            "ccy": "HKD", 
            "sessionToken": token2
        })
        ccyrateouttext = json.loads(ccyrateout.text) 
        if ccyrateouttext['result_code'] == 40011:
            ccyrateoutval = 1 
        else: 
            ccyrateoutval = ccyrateouttext['data']['recordData'][0]['rate'] # USD to HKD
        recordval2 = recordsize * execInfo.getPrice() * ccyrateoutval/ccyrateinval # Contract size multipled by number of points
        # self.info("SELL at $%.2f" % (execInfo.getPrice())) # In terms of points
        self.info("SELL at $%.2f" % (recordval2)) # Actual price

        currenttime = self.getCurrentDateTime()
        newinfo = {
                "Date": currenttime.date().strftime('%Y-%m-%d'), 
                "Time": currenttime.time().strftime('%H:%M:%S'), 
                "Action": "SELL", 
                "Price": recordval2
            }
        sellmoments.append(newinfo)
        self.__position = None

        self.__time = self.__time + 1
        print("New portfolio value: $%.2f" % self.getBroker().getCash())
        print(self.__time)
        
    def on_exit_canceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()

    def on_bars(self, bars):
        execInfo = bars[self.__instrument]
        produrl = ENDPOINT + PRODINFO
        productinfo = requests.post(produrl, 
        json = {
            "prodCode": self.__instrument, # Collects product code from sma_cross2, which collects from sma_strat2
            "sessionToken": token2,
            "dataRecordTotal": 100,
            "dataStartFromRecord": 0
        })
        recordDiction = json.loads(productinfo.text) 
        if recordDiction['result_code'] == 40011:
            recordsize = 0
            recordccy = "HKD"
        else:
            recordsize = recordDiction['data']['jsonData']['contractSize'] # Size of product
            recordccy = recordDiction['data']['jsonData']['ccy'] # Currency of product

        ccyrate = ENDPOINT + CCYRATES
        ccyratein = requests.post(ccyrate, 
        json = {
            "ccy": recordccy, # USD = 1
            "sessionToken": token2
        })
        ccyrateintext = json.loads(ccyratein.text) 
        if ccyrateintext['result_code'] == 40011:
            ccyrateinval = 1 
        else: 
            ccyrateinval = ccyrateintext['data']['recordData'][0]['rate'] # USD to recordccy
        ccyrateout = requests.post(ccyrate, 
        json = {
            "ccy": "HKD", 
            "sessionToken": token2
        })
        ccyrateouttext = json.loads(ccyrateout.text) 
        if ccyrateouttext['result_code'] == 40011:
            ccyrateoutval = 1 
        else: 
            ccyrateoutval = ccyrateouttext['data']['recordData'][0]['rate'] # USD to HKD
        recordval3 = recordsize * execInfo.getPrice() * ccyrateoutval/ccyrateinval # Contract size multipled by number of points
        
        # Reach end of self.__sma list or skip over if self.getBroker().getCash() will drop below given value
        if self.__sma[-1] is None:
        # if (self.__sma[-1] is None or self.getBroker().getCash() < boundaryValue): # Need to find way to limit number of positions
            return
        
        # If a position was not opened, check if we should enter a long position. # Heavily simplified version of SMA
        if self.__position is None:
            if cross.cross_above(self.__prices, self.__sma) > 0 and recordval3 != 0:

                alltrading = list(unique_everseen(alltrades))

                if buymoments and sellmoments:
                    def fun(l1, l2): # Apply for every pair that exists
                        for x,n in zip(l1, l2):
                            pnl = (x["Price"] - n["Price"])/x["Price"] # Applies P/L to each pair of buy and sell # If lists are uneven, extra values are not included
                            index = l2.index(n) # Assume that user cannot sell anything they have not bought
                            alltrades.append({"Trade Pair #": (index + 1), "Buy": n, "Sell": x, "P/L Value": '{:.4%}'.format(pnl)})
                        return alltrades
                    fun(sellmoments, buymoments)

                    alltrading = list(unique_everseen(alltrades)) # Removes duplicates
                print(alltrading)
                shares = int(self.getBroker().getCash() * 0.9 / recordval3) # Actual price
                # Enter a buy market order. The order is good till canceled.
                self.__position = self.enterLong(self.__instrument, shares, True)
                
        # Check if we have to exit the position.
        elif not self.__position.exitActive() and cross.cross_below(self.__prices, self.__sma) > 0:
            self.__position.exitMarket()