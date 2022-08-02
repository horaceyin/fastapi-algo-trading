from __future__ import division
from services.technical_analysis_service import PnLService
from schemas.technical_analysis_schemas import GetDoneTradeModel
import statistics
import pandas as pd

class Report(PnLService):

    def __init__(self, accName: str, date: str):
        super().__init__(accName)
        self.reportType = "report"
        self.date = date
        # super class attr: accName, col, tradeNum, totalDoneContract, _pnl

    #get the number of trade
    def __totaltrade(self,list):
        count = 0
        for _ in list:
            count = count+1
        return count
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
    
    # Get the sum of all pnl
    def __get_totalpnl(self, pnlList):
        res = 0
        for ele in pnlList:
            res += float(ele)
        return res

    def __get_totalreturns(self, returnlist):
        res = 0
        for ele in returnlist:
            res += float(ele)
        return res

    
    # Use statistics package to call the sd of a list
    def __get_sd(self, list):
        if len(list)==0:
            return 1
        else:
            return (statistics.stdev(list))

    @staticmethod
    def convtoperc(x):
        r = round(x, 3) * 100
        return r
    
    def get_report(self, request: GetDoneTradeModel):
        data = self.get_pnl(request) # Gets trading data for given target account within given timeframe; all data below is in chronological order
        pnl = []
        negativePnl = []
        positivePnl = []
        tradeNumber = 0
        returns = []
        positiveRet = []
        negativeRet = []
        for i in data:
            pnl +=data[i][0]['pnl']
            negativePnl += data[i][0]['negativePnl']
            positivePnl += data[i][0]['positivePnl']
            tradeNumber += data[i][0]['num']
            returns += data[i][0]['returns']
            print(returns)
            positiveRet += data[i][0]['positiveRet']
            negativeRet += data[i][0]['negativeRet']
            
        def avg_return_for_pnl(pnl, cost):
            try:
                result = self.convtoperc(self.__get_totalreturns(pnl)/self.__totaltrade(cost))
            except ZeroDivisionError:
                result = 0
            return result
        def profit():
            result = self.__get_totalpnl(positivePnl)/self.__totaltrade(positivePnl)
            return result
        def loss():
            try:
                result = self.__get_totalpnl(negativePnl)/self.__totaltrade(negativePnl)
            except ZeroDivisionError:
                result = 0
            return result
        #for overall P/L ratio if the list is empty
        def checkanswer():
            try:
                result = profit()/loss()
            except ZeroDivisionError:
                return profit()
            return result
        report = {
            'total': {
                "totalTrades": tradeNumber, # Including all trades 
                "avgProfit": (self.__get_totalpnl(pnl) / tradeNumber),
                "profitsStdDev": self.__get_sd(pnl),
                "minProfit": min(pnl, default=0),
                "maxProfit": max(pnl, default=0),
                "avgReturn": avg_return_for_pnl(returns,returns),
                "returnStdDev": self.__get_sd(returns), 
                "maxReturn": max(returns, default=0)*100,
                "minReturn": min(returns, default=0)*100,
                "overallP/LRatio": checkanswer(),
                "averageProfitabilityPerTrade": (self.__get_totalpnl(positivePnl) - self.__get_totalpnl(negativePnl))/tradeNumber
            },
            'profitable': {
                "profitableTrades": self.__totaltrade(positivePnl),
                "avgProfit": profit(),
                "profitsStdDev": self.__get_sd(positivePnl),
                "minProfit": min(positivePnl, default=0),
                "maxProfit": max(positivePnl, default=0),
                "avgReturn": avg_return_for_pnl(positiveRet, positivePnl), 
                "returnStdDev": self.__get_sd(positiveRet), 
                "maxReturn": max(positiveRet, default=0)*100,
                "minReturn": min(positiveRet, default=0)*100
            },
            'unprofitable': {
                "unprofitableTrades": self.__totaltrade(negativePnl),
                "avgLoss": loss(),
                "lossesStdDev": self.__get_sd(negativePnl),
                "minLoss": min(negativePnl, default=0),
                "maxLoss": max(negativePnl, default=0),
                "avgReturn": avg_return_for_pnl(negativeRet, negativePnl),
                "returnStdDev": self.__get_sd(negativeRet),
                "maxReturn": max(negativeRet, default=0)*100,
                "minReturn": min(negativeRet, default=0)*100
            }
        }

        # Sample code to make HTML
        # total = report["total"]
        # prof = report["profitable"]
        # unprof = report["unprofitable"]
        # t = pd.Series(total, name = "Total").to_frame()
        # p = pd.Series(prof, name = "Profitable").to_frame()
        # u = pd.Series(unprof, name = "Unprofitable").to_frame()

        # with open("report.html", 'w') as _file:
        #     _file.write(t.to_html() + "\n\n" + p.to_html() + "\n\n" + u.to_html())

        return report
        
        #total trade = total count of pnl
        #total pnl / total count of pnl = avg. profit
        #use statistics library to call sd
        #Max profit = Max number in pnl
        #Min profit = Min number in pnl
        #avg return = [total pnl / (buyRecordQueue * buyTradeNum) *100%] / total count of pnl
        #Return sd: 
        #First, cal the total pnl of one product. dataframeList[int]
        #Second, [total pnl of one product  / (buyRecordQueue * buyTradeNum) *100%] then get a list of returns.
        #Third, use statistics library to cal sd
        #
        #Max return = Max number in a list of returns
        #Min return = Min number in a list of returns

        #Profitable and Unprofitable = separate the total trade with one positive list and one negative list