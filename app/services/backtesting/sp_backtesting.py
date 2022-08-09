import abc
from ast import Return
from services.backtesting import sp_position
from matplotlib.pyplot import bar
from pyalgotrade.strategy import BacktestingStrategy
from schemas.backtesting.bar_summary_schemas import BarSummary
from services.backtesting.spbarfeed.sp_bar_feed import SpRowParser
from schemas.backtesting.backtesting_schemas import BacktestingModel
from services.backtesting.spbarfeed.sp_bar_feed import SpBarFeed
from services.broker.sp_broker import SPBroker
from services.backtesting.sp_indicators import SPIndicators
from pyalgotrade import strategy
from pyalgotrade.stratanalyzer import returns
from pyalgotrade.stratanalyzer import sharpe
from pyalgotrade.stratanalyzer import drawdown
from pyalgotrade.stratanalyzer import trades
from pyalgotrade.bar import Bars
from pyalgotrade import plotter
from pyalgotrade.stratanalyzer import sharpe
from pyalgotrade.bitstamp import broker

# class SPBroker(backtesting.Broker):
#     def __init__(self, portfolio_value, live_trade=True) -> None:
#         super().__init__(portfolio_value)

class SPBacktesting(BacktestingStrategy):
    
    def __init__(self, request: BacktestingModel, live_trade=False):
        self.__prod_indicator_list = request.prodCode # prodCode = [{name: str, indicators:[...]}]
        self.__portfolio_value = request.portfolioValue
        self.__boundary_value = request.boundaryValue
        self.__days = request.days
        self.__bar_summary = request.barSummary
        self.__live_trade = live_trade

        self.product_list = self.__create_product(self.__prod_indicator_list) # create list: ['HSIZ2', 'HSIN2']

        self.sp_bar_feed = SpBarFeed(self.product_list, self.__days, self.__bar_summary) # SpBarFeed(barSummary, loadedBars=[], timezone = None, maxLen = None) # No __ in front to allow usage outside
        self.sp_broker = SPBroker(self.__portfolio_value, self.__boundary_value, self.sp_bar_feed, live_trade)

        self.sp_indicators = SPIndicators(self.sp_bar_feed)
        self.sp_indicators.register_indicators(self.__prod_indicator_list)

        # for testing, product name: 'HSIZ2', 'HSIN2' 
        super(SPBacktesting, self).__init__(self.sp_bar_feed, self.sp_broker) # BacktestingStrategy(barFeed, cash_or_brk=1000000)
        self.__init_analyzer()


    def get_product_list(self):
        return self.product_list

    def get_indicators(self):
        return self.sp_indicators

    def get_sp_data(self):
        pass

    def __create_product(self, prod_indicator_list):
        if len(prod_indicator_list) == 0: return None

        product_list = [product.name for product in prod_indicator_list]

        return product_list

    def __init_analyzer(self):
        retAnalyzer = returns.Returns()
        self.attachAnalyzer(retAnalyzer)
        sharpeRatioAnalyzer = sharpe.SharpeRatio()
        self.attachAnalyzer(sharpeRatioAnalyzer)
        drawDownAnalyzer = drawdown.DrawDown()
        self.attachAnalyzer(drawDownAnalyzer)
        tradesAnalyzer = trades.Trades()
        self.attachAnalyzer(tradesAnalyzer)

    @property
    def get_prod_indicator_list(self):
        return self.__prod_indicator_list

    @get_prod_indicator_list.setter
    def get_prod_indicator_list(self, prod_code):
        self.__prod_indicator_list = prod_code

    @property
    def get_portfolio_value(self):
        return self.__portfolio_value

    @get_portfolio_value.setter
    def get_portfolio_value(self, port_val):
        if port_val > 0:
            if hasattr(self, 'sp_broker'):
                self.__portfolio_value = port_val
                self.sp_broker.get_portfolio_value(port_val)
            else:
                raise AttributeError(f'{type(self).__name__} does not have sp_broker attribute.')
        else:
            raise ValueError(f'portfolio should be larger than 0')

    @property
    def get_boundary_value(self):
        return self.__boundary_value

    @get_boundary_value.setter
    def get_boundary_value(self, bound_val):
        self.__boundary_value = bound_val

    @property
    def get_days(self):
        return self.__days

    @get_days.setter
    def get_days(self, days):
        self.__days = days

    @property
    def get_barSummary(self):
        return self.__barSummary

    @get_barSummary.setter
    def get_barSummary(self, bar_summary):
        self.__barSummary = bar_summary

    @property
    def get_position(self):
        return self.__position

    @get_position.setter
    def get_position(self, position):
        self.__position = position

    @property
    def get_live_trade(self):
        return self.__live_trade

    @get_live_trade.setter
    def get_live_trade(self, live_trade):
        self.__live_trade = live_trade

    @property
    def get_product_list(self):
        return self.product_list

    @get_product_list.setter
    def get_product_list(self, prod_list):
        self.product_list = prod_list

    @property
    def get_sp_bar_feed(self):
        return self.sp_bar_feed

    @get_sp_bar_feed.setter
    def get_sp_bar_feed(self, sp_bar_feed):
        self.sp_bar_feed = sp_bar_feed

    # getBroker already exists
    # @property
    # def get_sp_broker(self):
    #     return self.sp_broker

    # @get_sp_broker.setter
    # def get_sp_broker(self, sp_broker):
    #     self.sp_broker = sp_broker

    # @abc.abstractmethod
    # def onBars(self, bars, product_list, instrument): # SHOULD BE IMPLEMENTED BY FUTURE USERS
    #     # or implement a default strategy.
    #     return NotImplementedError
    def analyzer(self):
        retAnalyzer = returns.Returns()
        self.attachAnalyzer(retAnalyzer)
        sharpeRatioAnalyzer = sharpe.SharpeRatio()
        self.attachAnalyzer(sharpeRatioAnalyzer)
        drawDownAnalyzer = drawdown.DrawDown()
        self.attachAnalyzer(drawDownAnalyzer)
        tradesAnalyzer = trades.Trades()
        self.attachAnalyzer(tradesAnalyzer)

    def onBars(self, bars:Bars): #Default strategy
        smaPeriod = 15
        feed = self.sp_bar_feed
        for prod in self.product_list:
            strat = sp_position.Position(feed, prod, smaPeriod)
            # sharpeRatioAnalyzer = sharpe.SharpeRatio()
            # strat.attachAnalyzer(sharpeRatioAnalyzer)
            # print("Sharpe ratio: %.2f" % sharpeRatioAnalyzer.getSharpeRatio(0.05))
        # Strategy = sp_position.Position(feed, bars.getInstruments, smaPeriod)
        # returnAnalyzer = returns.Returns()
        # Strategy.attachAnalyzer(returnAnalyzer)
        # Strategy.run()
        # Strategy.info("Final portfolio value: $%.2f" % Strategy.getResult())
