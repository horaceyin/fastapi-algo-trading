from pyalgotrade import strategy
from pyalgotrade.technical import ma
from pyalgotrade.technical import cross

# from pyalgotrade.stratanalyzer import returns
# retAnalyzer = returns.Returns()

import requests
import json
import datetime

from core.config import SP_HOST_AND_PORT

from core.endpoints import ADMININFO
from services.backtesting.sma_datainfo import DataInfo
from schemas.backtesting_schemas import BacktestingModel
from os import environ
from dotenv import load_dotenv

# Access info from .env
ENDPOINT = SP_HOST_AND_PORT

class SMACrossOver(strategy.BacktestingStrategy): 
    def __init__(self, feed, instrument, smaPeriod, boundaryValue):
        super(SMACrossOver, self).__init__(feed)
        self.__instrument = instrument
        self.__position = None
        # We'll use adjusted close values instead of regular close values.
        #self.setUseAdjustedValues(True)
        self.__prices = feed[instrument].getPriceDataSeries()
        self.__sma = ma.SMA(self.__prices, smaPeriod)
        self.__time = 0
        self.__boundaryValue = boundaryValue # For boundary value below

    def onBars(self, bars):
        return super().onBars(bars)
        
    def get_sma(self):
        global access, token2, alltrades, buymoments, sellmoments
        accessurl = ENDPOINT + ADMININFO
        # Only required to be able to access system 
        # May fail due to server being unable to respond; currently testing potential 
        # TimeoutError: [WinError 10060] A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond
        #  (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x00000282A1E07CA0>: Failed to establish a new connection: [WinError 10061] No connection could be made because the target machine actively refused it'))
        
        requests.adapters.DEFAULT_RETRIES = 5 # Increase retries number
        s = requests.session()
        s.keep_alive = False # Disable keep alive
        access = s.post(accessurl, 
        json = {
            "password": "sp",
            "userId": "SPNICHOLAS",
            "apiAppId": "SP_F",
            "mode": 0
        }, verify=False, timeout=(5, 10))
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
        print ("Initial portfolio value: $%.2f" % self.getBroker().getCash()) # Gives initial portfolio value

    def on_enter_ok(self, position):
        global recordval1
        execInfo = position.getEntryOrder().getExecutionInfo()
        DataInfo(self.__instrument, token2).getInfo()
        # recordsize = DataInfo(self.__instrument, token2).recordSize()
        # ccyhkd = DataInfo(self.__instrument, token2).ccyRate()
        # recordval1 = recordsize * execInfo.getPrice() * ccyhkd # Contract size multipled by number of points in HKD
        recordval1 = execInfo.getPrice() # Number of points # TESTING CODE

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
        DataInfo(self.__instrument, token2).getInfo()
        # recordsize = DataInfo(self.__instrument, token2).recordSize()
        # ccyhkd = DataInfo(self.__instrument, token2).ccyRate()
        # recordval2 = recordsize * execInfo.getPrice() * ccyhkd # Contract size multipled by number of points
        recordval2 = execInfo.getPrice() # Number of points # TESTING CODE

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

    def onBars(self, bars):
        execInfo = bars[self.__instrument]
        DataInfo(self.__instrument, token2).getInfo()
        # recordsize = DataInfo(self.__instrument, token2).recordSize()
        # ccyhkd = DataInfo(self.__instrument, token2).ccyRate()
        # recordval3 = recordsize * execInfo.getPrice() * ccyhkd # Contract size multipled by number of points in HKD
        recordval3 = execInfo.getPrice() # Number of points # TESTING CODE
        
        # Reach end of self.__sma list or skip over if self.getBroker().getCash() will drop below given value
        # if self.__sma[-1] is None:
        if (self.__sma[-1] is None or self.getBroker().getCash() < self.__boundaryValue): # Need to find way to limit number of positions
            return
        
        # If a position was not opened, check if we should enter a long position. # Heavily simplified version of SMA
        if self.__position is None:
            if cross.cross_above(self.__prices, self.__sma) > 0 and recordval3 != 0:
                def duplremov(l, m):
                    seen = set()
                    for d in l:
                        t = tuple(sorted(d.items()))
                        if t not in seen:
                            seen.add(t)
                            m.append(d)

                alltrading = []
                duplremov(alltrades, alltrading)

                if buymoments and sellmoments:
                    def fun(l1, l2): # Apply for every pair that exists
                        for x,n in zip(l1, l2):
                            pnl = (x["Price"] - n["Price"])/x["Price"] # Applies P/L to each pair of buy and sell # If lists are uneven, extra values are not included
                            index = l2.index(n) # Assume that user cannot sell anything they have not bought
                            alltrades.append({"Trade Pair #": (index + 1), "Buy": n, "Sell": x, "P/L Value": '{:.4%}'.format(pnl)})
                        return alltrades
                    fun(sellmoments, buymoments)

                    duplremov(alltrades, alltrading)# Removes duplicates
                print(alltrading)
                shares = int(self.getBroker().getCash() * 0.9 / recordval3) # Actual price
                # Enter a buy market order. The order is good till canceled.
                self.__position = self.enterLong(self.__instrument, shares, True)
                
        # Check if we have to exit the position.
        elif not self.__position.exitActive() and cross.cross_below(self.__prices, self.__sma) > 0:
            self.__position.exitMarket()