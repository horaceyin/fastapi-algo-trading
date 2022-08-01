from pyalgotrade import broker as pbroker
from pyalgotrade.broker import backtesting
from services.sp_api_handler import SPAPIHandler
from schemas.order_api_schemas import AddOrder, AccessOrder

# To be accessed during either backtesting or actual trading

# @six.add_metaclass(metaclass=abc.ABCMeta)
class SPBroker(backtesting.Broker): # Inherit all properties and functions from broker
    def __init__(self, portfolio_value: float, bound_val: float, sp_bar_feed, live_trade: bool):
    # def __init__(self, request: UserLogin, portfolio_value, bound_val, sp_bar_feed, live_trade:bool=False):
        # Values transferred from SPBacktesting for backtesting.Broker
        self.__portfolio_value = portfolio_value 
        self.__sp_bar_feed = sp_bar_feed 

        # Values transferred from SPBacktesting for personal values
        self.__bound_val = bound_val # To limit how far portfolio value can drop; will stop trade once portfolio value reaches this point
        
        # Personal values
        self.__live_trade = live_trade # Either live trading (Order for program and for SPTrader) or non-live trading (Order for program only) 
        if live_trade == True:
            self.__sp_api_handler = SPAPIHandler()
        else:
            self.__sp_api_handler = None
        super(SPBroker, self).__init__(self.__portfolio_value, self.__sp_bar_feed, commission=None) # Used to call __init__ method of parent class backtesting.Broker; add additional variables below

    @property
    def get_portfolio_value(self):
        return self.__portfolio_value

    # def set_portfolio_value(self, portfolio_value):
    #     self.__portfolio_value = portfolio_value
    @get_portfolio_value.setter
    def get_portfolio_value(self, portfolio_value):
        self.__portfolio_value = portfolio_value

    @property
    def get_sp_bar_feed(self):
        return self.__sp_bar_feed

    # def set_sp_bar_feed(self, sp_bar_feed):
    #     self.__sp_bar_feed = sp_bar_feed
    @get_sp_bar_feed.setter
    def get_sp_bar_feed(self, sp_bar_feed):
        self.__sp_bar_feed = sp_bar_feed

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
    
    # # Client Portal API
    # Variables from backtesting.Broker
    def createMarketOrder(self, action, instrument, quantity, onClose):
        super().createMarketOrder(action, instrument, quantity, onClose)
        try:
            self.__sp_api_handler.createMarketOrder(action, instrument, quantity, onClose) # ASK SPTRADER HOW TO CREATE ORDER
            self.__sp_api_handler.activeOrder(action, instrument)
        except:
            pass

    def createLimitOrder(self, action, instrument, limitPrice, quantity):
        super().createLimitOrder(action, instrument, limitPrice, quantity)
        try:
            self.__sp_api_handler.createLimitOrder(action, instrument, limitPrice, quantity) # ASK SPTRADER HOW TO CREATE ORDER
            self.__sp_api_handler.activeOrder(action, instrument)
        except:
            pass

    def createStopOrder(self, action, instrument, stopPrice, quantity):
        super().createStopOrder(action, instrument, stopPrice, quantity)
        try:
            self.__sp_api_handler.createStopOrder(action, instrument, stopPrice, quantity) # ASK SPTRADER HOW TO CREATE ORDER
            self.__sp_api_handler.activeOrder(action, instrument)
        except:
            pass

    def createStopLimitOrder(self, action, instrument, stopPrice, limitPrice, quantity):
        super().createStopLimitOrder(action, instrument, stopPrice, limitPrice, quantity)
        try:
            self.__sp_api_handler.createStopLimitOrder(action, instrument, stopPrice, limitPrice, quantity) # ASK SPTRADER HOW TO CREATE ORDER
            self.__sp_api_handler.activeOrder(action, instrument)
        except:
            pass

    # Need to find way to cancel order with different formatting
    # order examples:
        # backtesting.MarketOrder(action, instrument, quantity, onClose, self.getInstrumentTraits(instrument))
        # backtesting.LimitOrder(action, instrument, limitPrice, quantity, self.getInstrumentTraits(instrument))
        # backtesting.StopOrder(action, instrument, stopPrice, quantity, self.getInstrumentTraits(instrument))
        # backtesting.StopLimitOrder(action, instrument, stopPrice, limitPrice, quantity, self.getInstrumentTraits(instrument))
    # Properties are inherited from request
    def cancelOrderSystem(self, order):
        super().cancelOrder(order)

    def cancelOrderAPI(self, accOrderNo, action, instrument):
        # request.sessionToken = self.__session_token
        try:
            self.__sp_api_handler.cancelOrder(accOrderNo, action, instrument)
        except:
            pass

    # Functions below are built such that they can only be done with the SP trading system
    def activeOrder(self, accOrderNo, action, instrument):
        # request.sessionToken = self.__session_token
        try:
            self.__sp_api_handler.activeOrder(accOrderNo, action, instrument)
        except:
            pass

    def inactiveOrder(self, accOrderNo, action, instrument):
        # request.sessionToken = self.__session_token
        try:
            self.__sp_api_handler.inactiveOrder(accOrderNo, action, instrument)
        except:
            pass
    
    def changeOrder(self, accOrderNo, buySell, instrument, price, quantity, stopPrice):
        # request.sessionToken = self.__session_token
        try:
            self.__sp_api_handler.changeOrder(accOrderNo, buySell, instrument, price, quantity, stopPrice)
        except:
            pass

    # # # Trader Admin API
    # def makeFuture(self, request: MakeFuture):
    #     try:
    #         self.__sp_api_handler.makeFuture(request)
    #     except:
    #         pass
