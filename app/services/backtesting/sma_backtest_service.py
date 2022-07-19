from services.backtesting.sma_simple_cross import SMACrossOver
from pyalgotrade import plotter
from pyalgotrade import broker
from pyalgotrade.barfeed import csvfeed
from pyalgotrade.bar import Frequency
from pyalgotrade.stratanalyzer import returns
from pyalgotrade.stratanalyzer import sharpe
from pyalgotrade.stratanalyzer import drawdown
from pyalgotrade.stratanalyzer import trades
from pyalgotrade.broker import backtesting
import pandas as pd
from datetime import datetime
import time
from common.common_helper import CommonHelper
from schemas.backtesting.backtesting_schemas import BacktestingModel
from services.backtesting.sma_datainfo import DataInfo

class sma_backtest:
    def __init__(self, instrument, day, second, smaPeriod, plot, startcash, barsum):
        self.__instrument = instrument
        self.__day = day
        self.__second = second
        self.__smaPeriod = smaPeriod
        self.__plot = plot
        self.__startcash = startcash
        self.__barsum = barsum

    # Formats text data for each trade
    @staticmethod
    def formatting_data(data):
        myData = data
        print(myData)
    # def formatting_data(status_code, text): # text of data; modify formatting from browser format
    #     if status_code < 400:
        # myData = text
        # tempData1 = myData.split(':')
        # tempData2 = tempData1[4].split(',0\r\n') # Remove 0 at end of each line
        # tempData3 = map(lambda bar: bar.split(','), tempData2) # Format data for processing in the future
        # newData = list(tempData3)
        # newData.pop()
        # for i, bar in enumerate(newData):
        #     oriDate = bar.pop()
        #     dateTime = datetime.fromtimestamp(int(oriDate))
        #     strDate = dateTime.strftime('%Y-%m-%d %H:%M:%S')
        #     bar.insert(0, strDate)
        # return newData



    def start_backtesting(self, request):
        date_time = datetime.fromtimestamp(int(time.time()))
        todayStrDate = date_time.strftime('%Y%m%d')
        csvName = f'{self.__instrument}-{todayStrDate}-sp.csv'

        URL = f'https://chart3.spsystem.info/pserver/chartdata_query.php?days={self.__day}&second={self.__second}&prod_code={self.__instrument}'

        # Frequency.TRADE: The bar represents a single trade.
        # Frequency.SECOND: The bar summarizes the trading activity during 1 second.
        # Frequency.MINUTE: The bar summarizes the trading activity during 1 minute.
        # Frequency.HOUR: The bar summarizes the trading activity during 1 hour.
        # Frequency.DAY: The bar summarizes the trading activity during 1 day.
        # Frequency.WEEK: The bar summarizes the trading activity during 1 week.
        # Frequency.MONTH: The bar summarizes the trading activity during 1 month.

        # Download the bars.
        myFeed = csvfeed.GenericBarFeed(Frequency.SECOND * self.__barsum) # 
        data = CommonHelper.post_url(URL, request)
        print(data)

        newData = sma_backtest.formatting_data(data)

        # print(newData)

        dateCol, openCol, highCol, lowCol, closeCol, volumeCol = DataInfo.construct_data(newData)

        pdData = {
            'Date Time': dateCol,
            'Open': openCol,
            'High': highCol,
            'Low': lowCol,
            'Close': closeCol,
            #'Adj Close': closeCol,
            'Volume': volumeCol
        }
        df = pd.DataFrame(pdData).set_index('Date Time')
        df.to_csv(csvName)
        print(len(dateCol))

        myFeed.addBarsFromCSV(self.__instrument, csvName)
        strat = SMACrossOver(myFeed, self.__instrument, self.__smaPeriod)

        strat.getBroker().setCash(self.__startcash) # Set new value of portfolio

        retAnalyzer = returns.Returns()
        strat.attachAnalyzer(retAnalyzer)

        sharpeRatioAnalyzer = sharpe.SharpeRatio()
        strat.attachAnalyzer(sharpeRatioAnalyzer)

        drawDownAnalyzer = drawdown.DrawDown()
        strat.attachAnalyzer(drawDownAnalyzer)

        tradesAnalyzer = trades.Trades()
        strat.attachAnalyzer(tradesAnalyzer)

        if self.__plot:
            plt = plotter.StrategyPlotter(strat, True, False, True)
            plt.getInstrumentSubplot(self.__instrument).addDataSeries("SMA", strat.get_sma())

        strat.run()
        DataInfo.print_result(strat, retAnalyzer, sharpeRatioAnalyzer, drawDownAnalyzer, tradesAnalyzer)

        if self.__plot:
            pass
            # plt.plot()