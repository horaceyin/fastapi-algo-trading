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
from services.backtesting.sma.sma_datainfo import DataInfo

# Access info from .env
ENDPOINT = SP_HOST_AND_PORT

### 

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

    # def onBars(self, bars):
    #     return super().onBars(bars)
        
    def get_sma(self):
        # Required to be able to access system information (e.g. User's portfolio, current currency exchange rates)
        global access, token2, alltrades, buymoments, sellmoments, productInfo
        accessurl = ENDPOINT + ADMININFO

        # CURRENTLY TAKING FAR TOO LONG TO LOAD AND END UP WITH NO CHANGES
        # requests.adapters.DEFAULT_RETRIES = 5 # Increase retries number
        # s = requests.session()
        # s.keep_alive = False # Disable keep alive
        # access = requests.post(accessurl, 
        # json = {
        #     "password": "sp",
        #     "userId": "SPNICHOLAS",
        #     "apiAppId": "SP_F",
        #     "mode": 0
        # }, timeout=10)
        # dataDict = json.loads(access.text) 
        try:
            access = requests.post(accessurl, 
            json = {
                "password": "sp",
                "userId": "SPNICHOLAS",
                "apiAppId": "SP_F",
                "mode": 0
            }, timeout=(10, 10))
            dataDict = json.loads(access.text) 
            token2 = dataDict['data']['sessionToken'] # Session token to access other requests
        except:
            raise SystemExit("The system currently cannot be accessed. Try testing again later.")
        # To transfer dictionary object to below
        # {'result_code': -1, 'result_msg': 'API REQUEST FAILED', 'timestamp': 1657503243, 'log_message': 'Error Class class com.sharppoint.apiSpadminWeb.controllers.user.AdminLoginContoller : nested exception is org.apache.ibatis.exceptions.PersistenceException: \r\n### Error updating database.  Cause: org.springframework.jdbc.CannotGetJdbcConnectionException: Failed to obtain JDBC Connection; nested exception is java.sql.SQLTransientConnectionException: HikariPool-1 - Connection is not available, request timed out after 30012ms.\r\n### The error may exist in class path resource [com/sharppoint/apiSpadminWeb/dao/mapper/userLog/UserLogMapper.xml]\r\n### The error may involve com.sharppoint.apiSpadminWeb.dao.orm.userLog.UserLogMapper.insertSelective\r\n### The error occurred while executing an update\r\n### Cause: org.springframework.jdbc.CannotGetJdbcConnectionException: Failed to obtain JDBC Connection; nested exception is java.sql.SQLTransientConnectionException: HikariPool-1 - Connection is not available, request timed out after 30012ms.'}
        alltrades = []

        # Sort moments below by date, then by time (Only used to display data below)
        buymoments = [] # Make list of dictionaries for buying moments 
        buymoments.sort(key = lambda x: datetime.strptime(x['Date'], '%Y-%m-%d'))
        buymoments.sort(key = lambda x: datetime.strptime(x['Time'], '%H-%M-%S'))
        
        sellmoments =[] # Make list of dictionaries for selling moments 
        sellmoments.sort(key = lambda x: datetime.strptime(x['Date'], '%Y-%m-%d'))
        sellmoments.sort(key = lambda x: datetime.strptime(x['Time'], '%H-%M-%S'))
        
        # Login for recordsize and ccyhkd
        productInfo = DataInfo(self.__instrument, token2).getInfo() 
        return self.__sma # <pyalgotrade.technical.ma.SMA object at 0x11c0644c0>

    def on_start(self):
        print ("Initial portfolio value: $%.2f" % self.getBroker().getCash()) # Gives initial portfolio value

    def on_enter_ok(self, position): # self is current pyalgotrade.bar.Bars
        # Getting order information
        execInfo = position.getEntryOrder().getExecutionInfo() 

        recordsize = DataInfo(self.__instrument, token2).recordSize(productInfo)
        ccyhkd = DataInfo(self.__instrument, token2).ccyRate(productInfo)

        # Contract size multipled by number of points in HKD
        recordval1 = recordsize * execInfo.getPrice() * ccyhkd 
        # recordval1 = execInfo.getPrice() # Number of points # TESTING CODE
        self.info("BUY at $%.2f" % (recordval1)) # Actual price # Trying to find quantity 
        # Error message is from https://github.com/gbeced/pyalgotrade/blob/master/pyalgotrade/broker/fillstrategy.py, line 323
        # order.getId() to get id of current trade

        # Collecting date and time information to add new trade and add to buymoments (Only used to display data below)
        currenttime = self.getCurrentDateTime()
        newinfo = {
                "Date": currenttime.date().strftime('%Y-%m-%d'), 
                "Time": currenttime.time().strftime('%H:%M:%S'), 
                "Action": "BUY", 
                "Price": recordval1
            }
        buymoments.append(newinfo)

        # Display new portfolio value
        self.__time += 1
        print ("New portfolio value: $%.2f" % self.getBroker().getCash())
        print(self.__time)

    def on_enter_canceled(self, position):
        self.__position = None
    
    def on_exit_ok(self, position): # self is current pyalgotrade.bar.Bars
        # Getting order information
        execInfo = position.getExitOrder().getExecutionInfo()
        
        recordsize = DataInfo(self.__instrument, token2).recordSize(productInfo)
        ccyhkd = DataInfo(self.__instrument, token2).ccyRate(productInfo)
        
        # Contract size multipled by number of points in HKD
        recordval2 = recordsize * execInfo.getPrice() * ccyhkd # Contract size multipled by number of points
        # recordval2 = execInfo.getPrice() # Number of points # TESTING CODE
        self.info("SELL at $%.2f" % (recordval2)) # Actual price

        # Collecting date and time information to add new trade and add to sellmoments (Only used to display data below)
        currenttime = self.getCurrentDateTime()
        newinfo = {
                "Date": currenttime.date().strftime('%Y-%m-%d'), 
                "Time": currenttime.time().strftime('%H:%M:%S'), 
                "Action": "SELL", 
                "Price": recordval2
            }
        sellmoments.append(newinfo)

        # Display new portfolio value
        self.__position = None
        self.__time += 1
        print("New portfolio value: $%.2f" % self.getBroker().getCash())
        print(self.__time)
        
    def on_exit_canceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()

    # Called when bar is created
    def onBars(self, bars): # self is current pyalgotrade.bar.Bars
        # Getting order information
        execInfo = bars[self.__instrument]

        recordsize = DataInfo(self.__instrument, token2).recordSize(productInfo)
        ccyhkd = DataInfo(self.__instrument, token2).ccyRate(productInfo)

        # Contract size multipled by number of points in HKD
        recordval3 = recordsize * execInfo.getPrice() * ccyhkd 
        # recordval3 = execInfo.getPrice() # Number of points # TESTING CODE
        
        # Reach end of self.__sma list or skip over if self.getBroker().getCash() will drop below given value
        # if self.__sma[-1] is None:
        if (self.__sma[-1] is None or self.getBroker().getCash() < self.__boundaryValue): # Need to find way to increase and limit number of positions
            return
        
        # If a position was not opened, check if we should enter a long position. # Heavily simplified version of SMA
        if self.__position is None:
            if cross.cross_above(self.__prices, self.__sma) > 0 and recordval3 != 0: # Line crosses over and recordval3 is not 0
                # Remove duplicates
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
                    if alltrading:
                        alltrading.pop() # To remove previous P/L ratio
                    def fun(l1, l2): # Apply for every pair that exists
                        for x,n in zip(l1, l2):
                            npm = (x["Price"] - n["Price"])/x["Price"] # Applies Net Profit Margin formula to each pair of buy and sell # If lists are uneven, extra values are not included
                            index = min(l1.index(x), l2.index(n))
                            alltrades.append({"Trade Pair #": (index + 1), "Buy": n, "Sell": x, "Net Profit Margin": '{:.4%}'.format(npm)})
                        return alltrades
                    fun(sellmoments, buymoments)
                    duplremov(alltrades, alltrading) # Removes duplicates
                    def results(l1, l2, l3):
                        def meanfunc(lst):
                            sum = 0
                            for m in lst:
                                sum += m["Price"]
                            mean = sum/len(lst)
                            return mean
                        pnl = meanfunc(l1)/meanfunc(l2)
                        appt = len(l1)/len(l3) * meanfunc(l1) - len(l2)/len(l3) * meanfunc(l2)
                        alltrading.append({"Current P/L Ratio": pnl, "Average Profitability per Trade": appt}) # Obtain current P/L  and average profitability of all trades
                    results(sellmoments, buymoments, alltrading)
                print(alltrading)
                shares = int(self.getBroker().getCash() * 0.9 / recordval3) # Actual price
                # Enter a buy market order. The order is good till canceled.
                self.__position = self.enterLong(self.__instrument, shares, True)
                
        # Check if we have to exit the position.
        elif not self.__position.exitActive() and cross.cross_below(self.__prices, self.__sma) > 0:
            self.__position.exitMarket()