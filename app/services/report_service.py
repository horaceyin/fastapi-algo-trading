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
    
    def __get_totalpnl(self, request):
        totalpnl=0
        for i in self.get_pnl(request):
            totalpnl+=i
        return totalpnl
    
    def __get_sd(self):
        return (statistics.stdev(self))

    @staticmethod
    def __max_min(pnl):
        min = pnl.index(min(pnl))
        max = pnl.index(max(pnl))
        return max, min


    @staticmethod
    def __cost(self, request):
        self.__cal_pnl(self)
        self.taHelper.get_pnl(request)
        return self.buyRecordQueue*self.buyTradeNum


    @classmethod
    def __avg_return(cls, listofpnl):
        avg_return = ((cls.__get_totalpnl(listofpnl) / cls.__cost())*100)
        return avg_return


    @classmethod
    def __avg_return_sd(cls,listofpnl):
        avg_return_sd = statistics.stdev(cls.__avg_return(listofpnl))
        return avg_return_sd
    
    def __max_min():
        pass


    def get_report(self, request: reportModel):
        self.__get_done_trade
        pass
        
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