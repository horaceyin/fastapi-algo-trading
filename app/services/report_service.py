from matplotlib.font_manager import json_load
from numpy import double, empty, negative
from services.technical_analysis_service import PnLService
from schemas.report_schemas import ReportModel
import statistics
import math

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

    # Get the buy cost of pnl to call the avg. return
    def __get_cost(self):
        buyPrice = []
        buyNum = []
        data = self.get_pnl() # From technical_analysis_service # Need posList, priceList
        buyPrice += data['posList']
        buyNum += data['priceList']
        result = 0
        res_list = [buyPrice[i] * buyNum[i] for i in range(len(buyPrice))]
        for i in res_list:
            result +=i
        return result                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
    
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

    @classmethod
    # Average of returns
    def __avg_return(cls, pnlList):
        avg_return = ((cls.__get_totalpnl(cls,pnlList) / cls.__get_cost(cls))*100)
        return avg_return
    # def __avg_return(cls, listofpnl, tradeRecordObj):
    #     buyprice = cls.__buy_price(tradeRecordObj)
    #     avg_return = ((cls.__get_totalpnl(listofpnl)/tradenum) * 100)
    #     # ((sell price - buy price)/ buy price)/total trade) = (Net return/Cost)/total trade * 100%
    #     return avg_return

    @staticmethod
    def convtoperc(x):
        r = round(x, 3) * 100
        return r
    
    def get_report(self, request: ReportModel):
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
            if negativePnl is empty:
                return negativePnl[0] #error when list is empty
            positivePnl += data[i][0]['positivePnl']
            if positivePnl is empty:
                return positivePnl[0]
            tradeNumber += data[i][0]['num']
            returns += data[i][0]['returns']
            positiveRet += data[i][0]['positiveRet']
            if positiveRet is empty:
                return positiveRet[0]
            negativeRet += data[i][0]['negativeRet']
            if negativeRet is empty:
                return negativeRet[0]
        def get_cost():
            buyPrice = []
            buyNum = []
            data = self.get_pnl(request) # From technical_analysis_service # Need posList, priceList
            for i in data:
                buyPrice += data[i][0]['posList']
                buyNum += data[i][0]['priceList']
            result = 0
            res_list = [buyPrice[i] * buyNum[i] for i in range(len(buyPrice))]
            for i in res_list:
                result +=i
            return result  
        def avg_return(pnlList):
            avg_return = (self.__get_totalpnl(pnlList) / get_cost())
            return avg_return
        def profit():
            result = self.__get_totalpnl(positivePnl)/self.__totaltrade(positivePnl)
            return result
        def loss():
            if self.__totaltrade(negativePnl) ==0:
                return 1
            else:
                return(self.__get_totalpnl(negativePnl)/self.__totaltrade(negativePnl))
        report = {
            # 'report':{
            #     "report_data":"messages
            #     "
            # }
            'total': {
                "Total trades": tradeNumber, # Including all trades 
                "Avg. Profit": (self.__get_totalpnl(pnl) / tradeNumber),
                "Profits. std. dev.": self.__get_sd(pnl)*100,
                "Min. Profit": min(pnl),
                "Max. Profit": max(pnl),
                "Avg. Return": avg_return(pnl),
                "Return std. dev.": self.__get_sd(returns)*100, # self.__return_std_dev(),
                "Max. Return": max(returns),
                "Min. Return": min(returns),
                "Overall P/L Ratio": profit() / loss(),
                "Average Profitability per Trade": (self.__get_totalpnl(positivePnl) - self.__get_totalpnl(negativePnl))/tradeNumber
            },
            'profitable': {
                "Profitable trades": self.__totaltrade(positivePnl),
                "Avg. profit": profit(),
                "Profits. std. dev.": self.__get_sd(positivePnl)*100,
                "Min. Profit": min(positivePnl),
                "Max. Profit": max(positivePnl),
                "Avg. Return": self.convtoperc(self.__get_totalreturns(positiveRet)/tradeNumber), 
                "Return std. dev.": self.__get_sd(positiveRet)*100, 
                "Max. Return": max(positiveRet),
                "Min. Return": min(positiveRet)
            },
            'unprofitable': {
                "Unprofitable trades": self.__totaltrade(negativePnl),
                "Avg. Loss": loss(),
                "Losses. std. dev.": self.__get_sd(negativePnl)*100,
                "Min. Loss": min(negativePnl),
                "Max. Loss": max(negativePnl),
                "Avg. Return": self.convtoperc(self.__get_totalreturns(negativeRet)/tradeNumber),
                "Return std. dev.": self.__get_sd(negativeRet)*100,
                "Max. Return": max(negativeRet),
                "Min. Return": min(negativeRet)
            }
        }
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