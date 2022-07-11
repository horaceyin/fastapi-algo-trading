from matplotlib.font_manager import json_load
from services.technical_analysis_service import PnLService
from schemas.report_schemas import reportModel
import statistics

class Report(PnLService):

    def __init__(self, accName: str, date: str):
        super().__init__(accName)
        self.reportType = "report"
        self.date = date
        # super class attr: accName, col, tradeNum, totalDoneContract, _pnl

    # Get the number of trades
    def __totaltrade(self,list):
        count: int
        for _ in list:
            count = count+1
        return count

    # Get the buy cost of pnl to call the avg. return
    def __get_cost(self):
        data = self.__data_for_pnl() # From technical_analysis_service # Need posList, priceList
        # How to get value?
        pass                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
    
    # Get the sum of all pnl
    def __get_totalpnl(self, pnlList):
        totalpnl: int
        for i in pnlList:
            totalpnl+=i # Add to total P/L
        return totalpnl

    def __get_totalreturns(self, returnlist):
        totalreturns: float
        for i in returnlist:
            totalreturns+=i # Add to total returns
        return totalreturns
    
    # Use statistics package to call the sd of a list
    def __get_sd(self):
        return (statistics.stdev(self))

    @classmethod
    # Average of returns
    def __avg_return(cls, listofpnl):
        avg_return = ((cls.__get_totalpnl(listofpnl) / cls.__cost())*100)
        return avg_return
    # def __avg_return(cls, listofpnl, tradeRecordObj):
    #     buyprice = cls.__buy_price(tradeRecordObj)
    #     avg_return = ((cls.__get_totalpnl(listofpnl)/tradenum) * 100)
    #     # ((sell price - buy price)/ buy price)/total trade) = (Net return/Cost)/total trade * 100%
    #     return avg_return

    @classmethod
    # Store the returns as a list then use statistics to call the return sd. https://www.geeksforgeeks.org/python-statistics-stdev/ (example)
    def __return_std_dev(cls, listofpnl):
        # Return sd: 
        # First, call the total pnl of one product. dataframeList[int]
        # Second, [total pnl of one product  / (buyRecordQueue * buyTradeNum) *100%] then get a list of returns. # Total pnl / cost of futures * 100%
        # Third, use statistics library to call sd
        total_pnl = cls.__get_totalpnl(listofpnl)
        finalresult = total_pnl/cls.__get_cost(listofpnl) # * 100%
        # SERVER IS DOWN, CURRENTLY CANNOT GET LIST OF RETURNS
        return_std_dev = statistics.stdev(finalresult)
        return return_std_dev

    @classmethod
    # Takes standard deviation of a list of pnl
    def __avg_return_sd(cls,listofpnl):
        avg_return_sd = statistics.stdev(cls.__avg_return(listofpnl))
        return avg_return_sd
    


    def get_report(self, request: reportModel):
        data = self.get_pnl(request)
        pnl = list(map(lambda x : x['pnl'],data))
        positivePnl = list(map(lambda x : x['positivePnl'],data)) # List of all positive Pnl
        negativePnl = list(map(lambda x : x['negativePnl'],data)) # List of all negative Pnl
        contractSize = list(map(lambda x : x['contractSize'],data)) # Currently not functioning properly
        tradeNumber = list(map(lambda x : x['num'],data)) # Total number of trades

        returns = list(map(lambda x : x['returns'],data))
        posreturns = list(map(lambda x : x['posreturns'],data))
        negreturns = list(map(lambda x : x['negreturns'],data))
        report = {{
        "Total trades": tradeNumber,
        "Avg. Profit": (self.__get_totalpnl(positivePnl+negativePnl)/tradeNumber),
        "Profits. std. dev.": self.__avg_return_sd(self.__get_totalpnl(positivePnl+negativePnl)),
        "Min. Profit": min(pnl),
        "Max. Profit": max(pnl),
        "Avg. Return": (self.__get_totalreturns(posreturns+negreturns)/tradeNumber), # self.__avg_return(), #((sell price - buy price)/ buy price)/total trade) = (Net return/Cost)/total trade * 100%
        "Return std. dev.": self.__avg_return_sd(self.__get_totalpnl(posreturns+negreturns)), # self.__return_std_dev(),
        "Max. Return": max(returns),
        "Min. Return": min(returns)
        },
        {
        "Profitable trades": self.__get_totalpnl(positivePnl),
        "Avg. profit": (self.__get_totalpnl(positivePnl)/self.__totaltrade(positivePnl)),
        "Profits. std. dev.": self.__avg_return_sd(self.__get_totalpnl(positivePnl)),
        "Min. Profit": min(positivePnl),
        "Max. Profit": max(positivePnl),
        "Avg. Return": (self.__get_totalreturns(posreturns)/tradeNumber), # self.__avg_return(),
        "Return std. dev.": self.__avg_return_sd(self.__get_totalpnl(posreturns)), # self.__return_std_dev(),
        "Max. Return": max(posreturns),
        "Min. Return": min(posreturns)   
        },
        {
        "Unprofitable trades": self.__get_totalpnl(negativePnl),
        "Avg. Loss": (self.__get_totalpnl(negativePnl)/self.__totaltrade(negativePnl)),
        "Losses. std. dev.": self.__avg_return_sd(self.__get_totalpnl(negativePnl)),
        "Min. Loss": min(negativePnl),
        "Max. Loss": max(negativePnl),
        "Avg. Return": (self.__get_totalreturns(negreturns)/tradeNumber),
        "Return std. dev.": self.__avg_return_sd(self.__get_totalpnl(negreturns)),
        "Max. Return": max(negreturns),
        "Min. Return": min(negreturns)
        }}
        # self.__get_done_trade
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