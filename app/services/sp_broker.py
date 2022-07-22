import six, abc, pyalgotrade
from pyalgotrade import broker as pbroker
from pyalgotrade.broker import backtesting
from app.services.auth_service import AuthService
from services.sp_api_handler import SPAPIHandler
import logging
import traceback
from fastapi import HTTPException, status, Request
from schemas.order_api_schemas import AddOrder

# To be accessed during either backtesting or actual trading

# @six.add_metaclass(metaclass=abc.ABCMeta)
class SPBroker(backtesting.Broker): # Inherit all properties and functions from broker
    # def __init__(self, barFeed, cash_or_brk=1000000, request: ):
        # broker = backtesting.Broker(cash_or_brk, barFeed) # More convieneient than pyalgotrade.
    def __init__(self, portfolio_value, bound_val, sp_bar_feed, live_trade:bool=False):
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
    
    # Variables from backtesting.Broker
    def createOrder(self, request: AddOrder, onClose=False):
        instrument = request.prodCode
        quantity = request.qty
        # action = [BUY, BUY_TO_COVER, SELL, SELL_SHORT]
        if request.buySell == "B":
            action = pbroker.Order.Action.BUY
            print("Buy action")
        elif request.buySell == "S":
            action = pbroker.Order.Action.SELL
            print("Sell action")
        else:
            raise SystemExit("Order given is not buy or sell")

        # # Get session token
        # if self.__live_trade == True:
        #     AuthService.user_login()

        # Market order
        if request.orderType == 6:
            # onClose if order should be filled as close to the closing price as possible
            if onClose is True and self.__barFeed.isIntraday():
                raise Exception("Market-on-close not supported with intraday feeds")
            backtesting.MarketOrder(action, instrument, quantity, onClose, self.getInstrumentTraits(instrument))
            try:
                self.__sp_api_handler.createMarketOrder(request)
            except:
                pass

        # Stop-limit order
        elif request.orderType == 0 and (request.condType == 1 or request.condType == 4 or request.condType == 6):
            stopPrice = request.stopPriceInDec
            limitPrice = request.priceInDec
            backtesting.StopLimitOrder(action, instrument, stopPrice, limitPrice, quantity, self.getInstrumentTraits(instrument))
            try:
                self.__sp_api_handler.createStopLimitOrder(request)
            except:
                pass

        # Limit order
        elif request.orderType == 0:
            limitPrice = request.priceInDec
            backtesting.LimitOrder(action, instrument, limitPrice, quantity, self.getInstrumentTraits(instrument))
            try:
                self.__sp_api_handler.createLimitOrder(request)
            except:
                pass
        
        # Stop order
        elif (request.condType == 1 or request.condType == 4 or request.condType == 6):
            stopPrice = request.stopPriceInDec
            backtesting.StopOrder(action, instrument, stopPrice, quantity, self.getInstrumentTraits(instrument))
            try:
                self.__sp_api_handler.createStopOrder(request)
            except:
                pass

    # Need to find way to cancel order with different formatting
    # order examples:
        # backtesting.MarketOrder(action, instrument, quantity, onClose, self.getInstrumentTraits(instrument))
        # backtesting.LimitOrder(action, instrument, limitPrice, quantity, self.getInstrumentTraits(instrument))
        # backtesting.StopOrder(action, instrument, stopPrice, quantity, self.getInstrumentTraits(instrument))
        # backtesting.StopLimitOrder(action, instrument, stopPrice, limitPrice, quantity, self.getInstrumentTraits(instrument))
    # Properties are inherited from request
    def cancelOrder(self, order):
        super().cancelOrder(order)
        try:
            self.__sp_api_handler.cancelOrder()
        except:
            pass

    # Functions below are built such that they can only be done with the SP trading system
    def activeOrder(self):
        try:
            self.__sp_api_handler.activeOrder()
        except:
            pass

    def inactiveOrder(self):
        try:
            self.__sp_api_handler.inactiveOrder()
        except:
            pass
    
    def changeOrder(self):
        try:
            self.__sp_api_handler.changeOrder()
        except:
            pass