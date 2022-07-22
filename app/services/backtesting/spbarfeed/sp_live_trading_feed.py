from distutils.log import error
from pyalgotrade.barfeed import csvfeed
from app.schemas.backtesting.backtesting_schemas import BacktestingModel
import pandas as pd
import requests
import json


class SpBarFeed(csvfeed.BarFeed, BacktestingModel):
    def __init__(self, barSummary, loadedBars=[], timezone = None, maxLen = None):
        self.__barSummary = barSummary
        self.__loadedBars = loadedBars
        super(SpBarFeed, self).__init__(timezone, maxLen)

    def addBarsFromJson(self):
        # Load the json-formated data
        data = SpGetData.get_data()
        prod_list = BacktestingModel.prodCode
        self.__loadedBars = []
        myData = pd.read_json(data, orient = 'index')
        newData = myData.to_csv(index = False)
        for bar_ in newData:
            self.__loadedBars.append(bar_)

        
        return self.addBarsFromSequence(prod_list, self.__loadedBars)

class SpGetData(SpBarFeed):
    def __init__(self, barSummary, loadedBars=[], timezone=None, maxLen=None):
        super().__init__(barSummary, loadedBars, timezone, maxLen)

        
    def get_data(self):
        days = BacktestingModel.days
        second = self.__barSummary
        prod_code = BacktestingModel.prodCode
        new_data : json
        for code in prod_code:
            URL = f'https://chart3.spsystem.info/pserver/chartdata_query.php?days={days}&second={second}&prod_code={code}'
            request = requests.get(URL)
            data = request.text
            parse_json = json.loads(data)
            while parse_json == ('19:-1:EMPTY RESULT!'):
                try:
                    continue
                except ValueError:
                    print('The result of' +code+' is empty!\r\n')
            new_data +=parse_json
        return new_data