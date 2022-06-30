from services.sma_simple_cross import SMACrossOver
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
import requests
from datetime import datetime
import time
import json

class sma_backtest:
    def __init__(self, instrument, day, second, smaPeriod, plot, startcash):
        self.__instrument = instrument
        self.__day = day
        self.__second = second
        self.__smaPeriod = smaPeriod
        self.__plot = plot
        self.__startcash = startcash

    # Formats text data for each trade
    def formattingData(status_code, text):
        if status_code < 400:
            myData = text
            tempData1 = myData.split(':')
            tempData2 = tempData1[4].split(',0\r\n')
            tempData3 = map(lambda bar: bar.split(','), tempData2)
            newData = list(tempData3)
            newData.pop()
            for i, bar in enumerate(newData):
                oriDate = bar.pop()
                dateTime = datetime.fromtimestamp(int(oriDate))
                strDate = dateTime.strftime('%Y-%m-%d %H:%M:%S')
                bar.insert(0, strDate)
        return newData

    # Create list for each column
    def constructData(dataList):
        dateCol = []
        openCol = []
        highCol = []
        lowCol = []
        closeCol = []
        volumeCol = []
        for bar in dataList:
            dateCol.append(bar[0])
            openCol.append(bar[1])
            highCol.append(bar[2])
            lowCol.append(bar[3])
            closeCol.append(bar[4])
            volumeCol.append(bar[5])
        return (dateCol, openCol, highCol, lowCol, closeCol, volumeCol)

    def print_result(strat, retAnalyzer, sharpeRatioAnalyzer, drawDownAnalyzer, tradesAnalyzer):
        print("")
        print("Final portfolio value: $%.2f" % strat.getResult())
        print("Cumulative returns: %.4f %%" % (retAnalyzer.getCumulativeReturns()[-1] * 100))
        print("Sharpe ratio: %.2f" % (sharpeRatioAnalyzer.getSharpeRatio(0.05)))
        print("Max. drawdown: %.4f %%" % (drawDownAnalyzer.getMaxDrawDown() * 100))
        print("Longest drawdown duration: %s" % (drawDownAnalyzer.getLongestDrawDownDuration()))

        print("")
        print("Total trades: %d" % (tradesAnalyzer.getCount()))
        if tradesAnalyzer.getCount() > 0:
            profits = tradesAnalyzer.getAll()
            print("Avg. profit: $%2.2f" % (profits.mean()))
            print("Profits std. dev.: $%2.2f" % (profits.std()))
            print("Max. profit: $%2.2f" % (profits.max()))
            print("Min. profit: $%2.2f" % (profits.min()))

            returns = tradesAnalyzer.getAllReturns()
            print("Avg. return: %2.3f %%" % (returns.mean() * 100))
            print("Returns std. dev.: %2.3f %%" % (returns.std() * 100))
            print("Max. return: %2.3f %%" % (returns.max() * 100))
            print("Min. return: %2.3f %%" % (returns.min() * 100))

        print("")
        print("Profitable trades: %d" % (tradesAnalyzer.getProfitableCount()))

        if tradesAnalyzer.getProfitableCount() > 0:
            profits = tradesAnalyzer.getProfits()
            print("Avg. profit: $%2.2f" % (profits.mean()))
            print("Profits std. dev.: $%2.2f" % (profits.std()))
            print("Max. profit: $%2.2f" % (profits.max()))
            print("Min. profit: $%2.2f" % (profits.min()))
            returns = tradesAnalyzer.getPositiveReturns()
            print("Avg. return: %2.3f %%" % (returns.mean() * 100))
            print("Returns std. dev.: %2.3f %%" % (returns.std() * 100))
            print("Max. return: %2.3f %%" % (returns.max() * 100))
            print("Min. return: %2.3f %%" % (returns.min() * 100))

        print("")
        print("Unprofitable trades: %d" % (tradesAnalyzer.getUnprofitableCount()))

        if tradesAnalyzer.getUnprofitableCount() > 0:
            losses = tradesAnalyzer.getLosses()
            print("Avg. loss: $%2.2f" % (losses.mean()))
            print("Losses std. dev.: $%2.2f" % (losses.std()))
            print("Max. loss: $%2.2f" % (losses.min()))
            print("Min. loss: $%2.2f" % (losses.max()))
            returns = tradesAnalyzer.getNegativeReturns()
            print("Avg. return: %2.3f %%" % (returns.mean() * 100))
            print("Returns std. dev.: %2.3f %%" % (returns.std() * 100))
            print("Max. return: %2.3f %%" % (returns.max() * 100))
            print("Min. return: %2.3f %%" % (returns.min() * 100))


    def start_backtesting(self):
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
        myFeed = csvfeed.GenericBarFeed(Frequency.SECOND * 5)
        res = requests.get(url = URL)

        newData = sma_backtest.formattingData(res.status_code, res.text)
        print(newData)

        dateCol, openCol, highCol, lowCol, closeCol, volumeCol = sma_backtest.constructData(newData)

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
            plt.getInstrumentSubplot(self.__instrument).addDataSeries("SMA", strat.getSMA())

        strat.run()
        sma_backtest.print_result(strat, retAnalyzer, sharpeRatioAnalyzer, drawDownAnalyzer, tradesAnalyzer)

        if self.__plot:
            plt.plot()