from pyalgotrade.technical import (
    atr,
    bollinger,
    cross,
    cumret,
    highlow,
    hurst,
    linebreak,
    linreg,
    ma,
    macd,
    ratio,
    roc,
    rsi,
    stats,
    stoch,
    vwap
)

class SPIndicators:
    def __init__(self, sp_bar_feed):
        self.__indicators = {} # user access like my_indicator["HSIM2"], return a list of indicators
        self.__feed = sp_bar_feed

    def get_indicators(self):
        return self.__indicators
    
    def __indicator_factory(self, product_name, indicator):
        ret_indicator = None

        indicator_name = indicator.indicatorName
        close_prices = self.__feed[product_name].getPriceDataSeries()

        match indicator_name:
            case 'sma':
                ret_indicator = ma.SMA(close_prices, indicator.period, indicator.maxLen)
            case 'ema':
                ret_indicator = ma.EMA(close_prices, indicator.period, indicator.maxLen)
            case 'wma':
                ret_indicator = ma.WMA(close_prices, indicator.weight, indicator.maxLen)
            case 'macd':
                ret_indicator = macd.MACD(close_prices, indicator.fastEMA, indicator.slowEMA, indicator.signalEMA, indicator.maxLen)
            case 'roc':
                ret_indicator = roc.RateOfChange(close_prices, indicator.valuesAge, indicator.maxLen)
            case 'rsi':
                ret_indicator = rsi.RSI(close_prices, indicator.period, indicator.maxLen)
            case 'bollinger bands':
                ret_indicator = bollinger.BollingerBands(close_prices, indicator.period, indicator.numStdDev, indicator.maxLen)

        return ret_indicator

    def __create_indicators(self, product_name, indicators_list):
        ret_indicators = []

        for indicator_obj in indicators_list:
            indicator = self.__indicator_factory(product_name, indicator_obj)
            ret_indicators.append(indicator)

        return ret_indicators

    def register_indicators(self, product_list): #product_list = [{name: str, indicators:[...]}]
        if product_list is not None:
            for product in product_list:
                name = product.name #product name. e.g. HSIZ4 ...
                indicators_list = product.indicators
                self.__indicators.setdefault(name, self.__create_indicators(name, indicators_list))