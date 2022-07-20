import six, abc, pyalgotrade
from pyalgotrade import broker as pbroker
from pyalgotrade.broker import backtesting
from services.sp_api_handler import SPAPIHandler
import logging
import traceback
from fastapi import HTTPException, status, Request
from schemas.order_api_schemas import AddOrder, DeleteOrder

# To be accessed during either backtesting or actual trading

# @six.add_metaclass(metaclass=abc.ABCMeta)
class SPBroker(backtesting.Broker): # Inherit all properties and functions from broker
    # def __init__(self, barFeed, cash_or_brk=1000000, request: ):
        # broker = backtesting.Broker(cash_or_brk, barFeed) # More convieneient than pyalgotrade.
    def __init__(self, portfolio_value, bound_val, sp_bar_feed, live_trade:bool=False):
        # Values transferred from SPBacktesting for backtesting.Broker
        self.__portfolio_value = portfolio_value # May not be neccessary
        self.__sp_bar_feed = sp_bar_feed # May not be neccessary

        # Values transferred from SPBacktesting for personal values
        self.__bound_val = bound_val # To limit how far portfolio value can drop; will stop trade once portfolio value reaches this point
        
        # Personal values
        self.__live_trade = live_trade # Either live trading (Order for program and for SPTrader) or non-live trading (Order for program only) 
        if live_trade == True:
            self.__sp_api_handler = SPAPIHandler()
        super(SPBroker, self).__init__(portfolio_value, sp_bar_feed, commission=None) # Used to call __init__ method of parent class backtesting.Broker; add additional variables below

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
    def createMarketOrder(self, request: AddOrder, onClose=False):
    # def createMarketOrder(self, action, instrument, quantity, onClose=False):
        instrument = request.prodCode
        quantity = request.qty
        # action = [BUY, BUY_TO_COVER, SELL, SELL_SHORT]
        if request.buySell == "B":
            action = pbroker.Order.Action.BUY
        else:
            action = pbroker.Order.Action.SELL
        if onClose is True and self.__barFeed.isIntraday():
            raise Exception("Market-on-close not supported with intraday feeds")
        backtesting.MarketOrder(action, instrument, quantity, onClose, self.getInstrumentTraits(instrument)) 
        
        try:
            self.__sp_api_handler.createMarketOrder()
        except:
            pass
        # if self.__liveTrade is False:
        #     return backtesting.MarketOrder(action, instrument, quantity, onClose, self.getInstrumentTraits(instrument))
        # else:
        #     SPAPIHandler().createMarketOrder()
            # pass # Replace with code to access SP backtesting 
    
    def createLimitOrder(self, request: AddOrder):
    # def createLimitOrder(self, action, instrument, limitPrice, quantity):
        instrument = request.prodCode
        quantity = request.qty
        # action = [BUY, BUY_TO_COVER, SELL, SELL_SHORT]
        if request.buySell == "B":
            action = pbroker.Order.Action.BUY
        else:
            action = pbroker.Order.Action.SELL
        limitPrice = request.priceInDec
        backtesting.LimitOrder(action, instrument, limitPrice, quantity, self.getInstrumentTraits(instrument))
        try:
            self.__sp_api_handler.createLimitOrder()
        except:
            pass
        # if self.__liveTrade is False:
        #     return backtesting.LimitOrder(action, instrument, limitPrice, quantity, self.getInstrumentTraits(instrument))
        # else:
        #     SPAPIHandler().createLimitOrder()
            # pass # Replace with code to access SP backtesting
    
    def createStopOrder(self, request: AddOrder):
    # def createStopOrder(self, action, instrument, stopPrice, quantity):
        instrument = request.prodCode
        quantity = request.qty
        # action = [BUY, BUY_TO_COVER, SELL, SELL_SHORT]
        if request.buySell == "B":
            action = pbroker.Order.Action.BUY
        else:
            action = pbroker.Order.Action.SELL
        stopPrice = request.stopPriceInDec
        backtesting.StopOrder(action, instrument, stopPrice, quantity, self.getInstrumentTraits(instrument))
        try:
            self.__sp_api_handler.createStopOrder()
        except:
            pass
        # if self.__liveTrade is False:
        #     return backtesting.StopOrder(action, instrument, stopPrice, quantity, self.getInstrumentTraits(instrument))
        # else:
        #     SPAPIHandler().createStopOrder()
            # pass # Replace with code to access SP backtesting
    
    def createStopLimitOrder(self, request: AddOrder):
    # def createStopLimitOrder(self, action, instrument, stopPrice, limitPrice, quantity):
        instrument = request.prodCode
        quantity = request.qty
        # action = [BUY, BUY_TO_COVER, SELL, SELL_SHORT]
        if request.buySell == "B":
            action = pbroker.Order.Action.BUY
        else:
            action = pbroker.Order.Action.SELL
        stopPrice = request.stopPriceInDec
        limitPrice = request.priceInDec
        backtesting.StopLimitOrder(action, instrument, stopPrice, limitPrice, quantity, self.getInstrumentTraits(instrument))
        try:
            self.__sp_api_handler.createStopLimitOrder()
        except:
            pass
        # if self.__liveTrade is False:
        #     return backtesting.StopLimitOrder(action, instrument, stopPrice, limitPrice, quantity, self.getInstrumentTraits(instrument))
        # else:
        #     SPAPIHandler().createStopLimitOrder()
        #     # pass # Replace with code to access SP backtesting

    def cancelOrder(self, order):
        super().cancelOrder(order)
        try:
            self.__sp_api_handler.createStopLimitOrder()
        except:
            pass