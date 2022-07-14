import six, abc, pyalgotrade
from pyalgotrade.broker import backtesting

# @six.add_metaclass(metaclass=abc.ABCMeta)
class SPBroker(backtesting.Broker): # Inherit all properties and functions from broker
    # def __init__(self, barFeed, cash_or_brk=1000000, request: ):
        # broker = backtesting.Broker(cash_or_brk, barFeed) # More convieneient than pyalgotrade.
    def __init__(self, portfolio_value, boundVal, liveTrade=False):
        super(SPBroker, self).__init__(cash, barFeed, commission=None) # Used to call __init__ method of parent class backtesting.Broker; add additional variables below
        self.__portfolio_value = portfolio_value # Should be equal to cash
        self.__boundVal = boundVal # To limit how far portfolio value can drop; will stop trade once portfolio value reaches this point
        self.__liveTrade = liveTrade # Either live trading (Order for program and for SPTrader) or non-live trading (Order for program only) 

    def getBoundVal(self):
        return self.__boundVal

    def setBoundVal(self, boundVal):
        self.__boundVal = boundVal
    
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