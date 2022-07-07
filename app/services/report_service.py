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

    def __get_totaltrade(self):
        count=0
        for _ in self:
            count=count+1
        return count
    
    def __get_totalpnl(self, pnlList):
        totalpnl: int
        for i in pnlList:
            totalpnl+=i
        return totalpnl
    
    def __get_sd(self):
        return (statistics.stdev(self))

    @staticmethod
    def __max(pnl):
        max = pnl.index(max(pnl))
        return max

    def __min(pnl):
        min = pnl.index(min(pnl))
        return min

    @staticmethod
    def __cost(self, request):
        self.__cal_pnl(self)
        self.taHelper.get_pnl(request)
        return self.buyRecordQueue*self.buyTradeNum


    @classmethod
    def __avg_return(cls, listofpnl):
        avg_return = ((cls.__get_totalpnl(listofpnl) / cls.__cost())*100)
        return avg_return

    def __return_std_dev(self):
        pass

    @classmethod
    def __avg_return_sd(cls,listofpnl):
        avg_return_sd = statistics.stdev(cls.__avg_return(listofpnl))
        return avg_return_sd
    
    def __max_return():
        pass

    def __min_return():
        pass


    def get_report(self, request: reportModel):
        data = self.get_pnl(request)
        pnl = list(map(lambda x : x['pnl'],data))
        positivePnl = list(map(lambda x : x['positivePnl'],data))
        negativePnl = list(map(lambda x : x['negativePnl'],data))
        contractSize = list(map(lambda x : x['contractSize'],data))
        tradeNumber = list(map(lambda x : x['num'],data))
        # report = {{
        # "Total trades": self.__get_totaltrade(),
        # "Avg. profit": (self.__get_totalpnl()/self.__get_totaltrade()),
        # "Profits. std. dev.": self.__avg_return_sd,
        # "Max. profit": self.__min(),
        # "Max. profit": self.__max(),
        # "Avg. return": self.__avg_return,
        # "Return std. dev.": self.__return_std_dev,
        # "Max. Return": self.__max_return,
        # "Min. Return": self.__min_return
        # },
        # {
        # "Profitable trades": self.__get_totaltrade(),
        # "Avg. profit": (self.__get_totalpnl()/self.__get_totaltrade()),
        # "Profits. std. dev.": self.__avg_return_sd,
        # "Max. profit": self.__min(),
        # "Max. profit": self.__max(),
        # "Avg. return": self.__avg_return,
        # "Return std. dev.": self.__return_std_dev,
        # "Max. Return": self.__max_return,
        # "Min. Return": self.__min_return   
        # },
        # {
        # "Unprofitable trades": self.__get_totaltrade(),
        # "Avg. loss": (self.__get_totalpnl()/self.__get_totaltrade()),
        # "Losses. std. dev.": self.__avg_return_sd,
        # "Max. Loss": self.__min(),
        # "Max. Loss": self.__max(),
        # "Avg. return": self.__avg_return,
        # "Return std. dev.": self.__return_std_dev,
        # "Max. Return": self.__max_return,
        # "Min. Return": self.__min_return
        # }}
        # self.__get_done_trade
        return pnl
        
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