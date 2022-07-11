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

    #get the number of trade
    def __totaltrade(self,list):
        count: int
        for _ in list:
            count = count+1
        return count

    #get the buy cost of pnl to cal the avg. return
    def __get_cost(self):
        data = self.__data_for_pnl
        pass                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
    
    #get the total of pnl
    def __get_totalpnl(self, pnlList):
        totalpnl: int
        for i in pnlList:
            totalpnl+=i
        return totalpnl
    

    #use statistics package to cal the sd.
    def __get_sd(self):
        return (statistics.stdev(self))



    @classmethod
    def __avg_return(cls, listofpnl):
        avg_return = ((cls.__get_totalpnl(listofpnl) / cls.__get_cost)*100)
        return avg_return

    #store the returns as a list then use statistics to cal the return sd. https://www.geeksforgeeks.org/python-statistics-stdev/ (example)
    def __return_std_dev(self):
        pass

    @classmethod
    def __avg_return_sd(cls,listofpnl):
        avg_return_sd = statistics.stdev(cls.__avg_return(listofpnl))
        return avg_return_sd
    


    def get_report(self, request: reportModel):
        data = self.get_pnl(request)
        pnl = list(map(lambda x : x['pnl'],data))
        positivePnl = list(map(lambda x : x['positivePnl'],data))
        negativePnl = list(map(lambda x : x['negativePnl'],data))
        contractSize = list(map(lambda x : x['contractSize'],data))
        tradeNumber = list(map(lambda x : x['num'],data))
        report = {{
        "Total trades": tradeNumber,
        "Avg. profit": (self.__get_totalpnl (positivePnl+negativePnl) / tradeNumber),
        "Profits. std. dev.": self.__avg_return_sd (self.__get_totalpnl(positivePnl+negativePnl)),
        "Min. profit": min(pnl),
        "Max. profit": max(pnl),
        "Avg. return": self.__avg_return,
        "Return std. dev.": self.__return_std_dev,
        "Max. Return": max(),
        "Min. Return": min()
        },
        {
        "Profitable trades": self.__get_totalpnl(positivePnl),
        "Avg. profit": (self.__get_totalpnl(positivePnl)/self.__totaltrade(positivePnl)),
        "Profits. std. dev.": self.__avg_return_sd (self.__get_totalpnl(positivePnl)),
        "Min. profit": min(positivePnl),
        "Max. profit": max(positivePnl),
        "Avg. return": self.__avg_return,
        "Return std. dev.": self.__return_std_dev,
        "Max. Return": max(),
        "Min. Return": min()   
        },
        {
        "Unprofitable trades": self.__get_totalpnl(negativePnl),
        "Avg. loss": (self.__get_totalpnl(negativePnl)/self.__totaltrade(negativePnl)),
        "Losses. std. dev.": self.__avg_return_sd(self.__get_totalpnl(negativePnl)),
        "Min. Loss": min(negativePnl),
        "Max. Loss": max(negativePnl),
        "Avg. return": self.__avg_return,
        "Return std. dev.": self.__return_std_dev,
        "Max. Return": max(),
        "Min. Return": min()
        }}
        # self.__get_done_trade
        return report
        
        #total trade = total count of pnl
        #total pnl / total count of pnl = avg. profit
        #use statistics library to cal sd
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