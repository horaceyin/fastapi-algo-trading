from pyalgotrade.barfeed import csvfeed
import pandas as pd
from app.services.backtesting.sp_backtesting import SPBacktesting

class SpFeed(SPBacktesting,csvfeed.BarFeed):
    def __init__(self, timezone = None, maxLen = None, loadedBars=[]):
        data = SPBacktesting()
        self.__loadedBars = loadedBars
        self.__barSummary = data.get_barSummary
        self.__getProList = data.get_prod_list
        super(SpFeed, self).__init__(timezone, maxLen)


    def addBarsFromJson(self):
        # Load the json-formated data
        self.__loadedBars = []
        myData = pd.read_json(self.__barSummary, orient = 'index')
        newData = myData.to_csv(index = False)
        for bar_ in newData:
            self.__loadedBars.append(bar_)

        
        return self.addBarsFromSequence(self.__getProList, self.__loadedBars)