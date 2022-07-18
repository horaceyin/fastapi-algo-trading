from distutils.log import debug
import numpy as np
import pandas as pd
import math as m
import datetime
import quantopian.optimize as opt

class SPIndicators:
    def __init__(self, indicators):
        self.__indicators_list = None


    def SMA(data, n):
        data[n] = data["Close"].rolling(n).mean()
        
        return data


    #WMA no certain solution
    def RSI(data):
        delta = data['Close'].diff()
        up = delta.clip(lower=0)
        down = -1*delta.clip(upper=0)
        ema_up = up.ewm(com = 13, adjust = False).mean()
        ema_down = down.ewm(com = 13, adjust = False).mean()
        RSI = ema_up/ema_down
        data['RSI'] = RSI

        return data

    def ROC(data, n):
        M = data['Close'].diff(n-1)
        N = data['Close'].shift(n-1)
        ROC = pd.Series(M/N, name = 'ROC_' + str(n))
        data['ROC'] = ROC

        return data
    

    def MACD(data, n_fast, n_slow):
        EMAfast = pd.Series(pd.ewma(data['Close'], span = n_fast, min_periods = n_slow - 1))
        EMAslow = pd.Series(pd.ewma(data['Close'], span = n_slow, min_periods = n_slow - 1))
        MACD = pd.Series(EMAfast - EMAslow, name = 'MACD_' + str(n_fast) + '_' + str(n_slow))  
        MACDsign = pd.Series(pd.ewma(MACD, span = 9, min_periods = 8), name = 'MACDsign_' + str(n_fast) + '_' + str(n_slow))  
        MACDdiff = pd.Series(MACD - MACDsign, name = 'MACDdiff_' + str(n_fast) + '_' + str(n_slow))
        data['MACD'] = MACD
        data['MACDsign'] = MACDsign
        data['MACDdiff'] = MACDdiff

        return data

    def BOLLINGER(data, n):
        MA = pd.Series(pd.rolling_mean(data['Close'], n))
        MSD = pd.Series(pd.rolling_std(data['Close'], n))
        b1 = 4*MSD/MA
        B1 = pd.Series(b1, name = 'BOLLINGERB_' + str(n))
        data['B1'] = B1
        b2 = (data['Close'] - MA + 2* MSD)/ (4*MSD)
        B2 = pd.Series(b2, name = 'BOLLINGER%b_' + str(n))
        data['B2'] = B2
        
        return data