import six, abc, pyalgotrade
from pyalgotrade.broker import backtesting

# To be accessed during either backtesting or actual trading

# @six.add_metaclass(metaclass=abc.ABCMeta)
class SPBroker(backtesting.Broker): # Inherit all properties and functions from broker
    # def __init__(self, barFeed, cash_or_brk=1000000, request: ):
        # broker = backtesting.Broker(cash_or_brk, barFeed) # More convieneient than pyalgotrade.
    def __init__(self, portfolio_value, bound_val, sp_bar_feed, live_trade=False):
        # Values transferred from SPBacktesting for backtesting.Broker
        self.__portfolio_value = portfolio_value # May not be neccessary
        self.__sp_bar_feed = sp_bar_feed # May not be neccessary

        # Values transferred from SPBacktesting for personal values
        self.__bound_val = bound_val # To limit how far portfolio value can drop; will stop trade once portfolio value reaches this point
        
        # Personal values
        self.__live_trade = live_trade # Either live trading (Order for program and for SPTrader) or non-live trading (Order for program only) 
        super(SPBroker, self).__init__(portfolio_value, sp_bar_feed, commission=None) # Used to call __init__ method of parent class backtesting.Broker; add additional variables below

# Part of backtesting.Broker
    # @property # portfolio_value = cash in backtesting.Broker
    # def get_portfolio_value(self):
    #     return self.__portfolio_value

    # # def set_portfolio_value(self, portfolio_value):
    # #     self.__portfolio_value = portfolio_value
    # @get_portfolio_value.setter
    # def get_portfolio_value(self, portfolio_value):
    #     self.__portfolio_value = portfolio_value

    # @property # sp_bar_feed = barFeed in backtesting.Broker
    # def get_sp_bar_feed(self):
    #     return self.__sp_bar_feed

    # # def set_sp_bar_feed(self, sp_bar_feed):
    # #     self.__sp_bar_feed = sp_bar_feed
    # @get_sp_bar_feed.setter
    # def get_sp_bar_feed(self, sp_bar_feed):
    #     self.__sp_bar_feed = sp_bar_feed

    @property
    def get_bound_val(self):
        return self.__bound_val

    # def set_bound_val(self, bound_val):
    #     self.__bound_val = bound_val
    @get_bound_val.setter
    def get_bound_val(self, bound_val):
        self.__bound_val = bound_val
    
    @property
    def get_live_trade(self):
        return self.__live_trade

    # def set_live_trade(self, live_trade):
    #     self.__boundVal = live_trade
    @get_live_trade.setter
    def get_live_trade(self, live_trade):
        self.__live_trade = live_trade
    
    # Variables from backtesting.Broker
    def createMarketOrder(self, action, instrument, quantity, onClose=False):
        if onClose is True and self.__barFeed.isIntraday():
            raise Exception("Market-on-close not supported with intraday feeds")
        if self.__liveTrade is False:
            return backtesting.MarketOrder(action, instrument, quantity, onClose, self.getInstrumentTraits(instrument))
        else:
            pass # Replace with code to access SP backtesting 
    
    def createLimitOrder(self, action, instrument, limitPrice, quantity):
        if self.__liveTrade is False:
            return backtesting.LimitOrder(action, instrument, limitPrice, quantity, self.getInstrumentTraits(instrument))
        else:
            pass # Replace with code to access SP backtesting
    
    def createStopOrder(self, action, instrument, stopPrice, quantity):
        if self.__liveTrade is False:
            return backtesting.StopOrder(action, instrument, stopPrice, quantity, self.getInstrumentTraits(instrument))
        else:
            pass # Replace with code to access SP backtesting
    
    def createStopLimitOrder(self, action, instrument, stopPrice, limitPrice, quantity):
        if self.__liveTrade is False:
            return backtesting.StopLimitOrder(action, instrument, stopPrice, limitPrice, quantity, self.getInstrumentTraits(instrument))
        else:
            pass # Replace with code to access SP backtesting

    def cancelOrder(self, order):
        return super().cancelOrder(order)