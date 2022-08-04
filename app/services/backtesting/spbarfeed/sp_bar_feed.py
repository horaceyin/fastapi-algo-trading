from pyalgotrade.barfeed import csvfeed
from pyalgotrade.bar import Frequency
from pyalgotrade import bar
from pyalgotrade.utils import dt
from pyalgotrade.utils import csvutils
from services.backtesting.spbarfeed.sp_data import SpData
from schemas.backtesting.bar_summary_schemas import BarSummary
from datetime import datetime, timedelta
from collections import deque
import six

# Frequency.TRADE: The bar represents a single trade.
# Frequency.SECOND: The bar summarizes the trading activity during 1 second.
# Frequency.MINUTE: The bar summarizes the trading activity during 1 minute.
# Frequency.HOUR: The bar summarizes the trading activity during 1 hour.
# Frequency.DAY: The bar summarizes the trading activity during 1 day.
# Frequency.WEEK: The bar summarizes the trading activity during 1 week.
# Frequency.MONTH: The bar summarizes the trading activity during 1 month.

frequency_dict = {
    'month': Frequency.MONTH,
    'week': Frequency.WEEK,
    'day': Frequency.DAY,
    'hour': Frequency.HOUR,
    'minute': Frequency.MINUTE,
    'second': Frequency.SECOND   
}

class SpBarFeed(csvfeed.BarFeed):
    def __init__(self, prod_list, days, bar_summary, timezone=None, maxLen=None):
        self.__prod_list = prod_list
        self.__days = days
        self.__bar_summary = bar_summary
        self.__sp_data = SpData()

        self.__timezone = timezone
        self.__have_adj_close = False
        self.__bar_class = bar.BasicBar
        self.__date_time_format = "%Y-%m-%d %H:%M:%S"
        
        # bar's column names, adj_close set to None if it's unnecessary
        # error appear if adj_close is deleted
        self.__column_names = {
            "datetime": "T",
            "open": "O",
            "high": "H",
            "low": "L",
            "close": "C",
            "volume": "V",
            "adj_close": None
        }
        frequency, time = self.__create_frequency(self.__bar_summary)
        self.__interval = frequency * time
        super(SpBarFeed, self).__init__(frequency * time, maxLen = maxLen)
        
        # create bars and add to BarFeed
        self.__create_bars()

    def getDailyBarTime(self):
        if self.__bar_summary.day:
            # if daily bar use
            return super().getDailyBarTime()
        else: return None

    def get_interval(self):
        return self.__interval

    def barsHaveAdjClose(self):
        return self.__have_adj_close

    def set_no_adj_close(self):
        self.__column_names["adj_close"] = None
        self.__have_adj_close = False

    def set_column_name(self, col, name):
        self.__column_names[col] = name

    def set_datetime_format(self, date_time_format):
        """
        Set the format string to use with strptime to parse datetime column.
        """
        self.__date_time_format = date_time_format

    # fetch price data in json and register it in BarFeed
    def add_bars_from_json(self, prod_code, days, seconds, row_parser, skip_malformed_bars=False):

        def parse_bar_skip_malformed(row):
            ret = None
            try:
                ret = row_parser.parseBar(row)
            except Exception:
                pass
            return ret

        # set parser function
        if skip_malformed_bars:
            parse_bar = parse_bar_skip_malformed
        else:
            parse_bar = row_parser.parseBar
        
        # Load the json-formated data from sp price server
        self.__sp_data.set_prod_code(prod_code)
        self.__sp_data.set_days_before(days)
        self.__sp_data.set_bar_seconds(seconds)
        raw_data = self.__sp_data.get_sp_data()
        
        # a series of BasicBar object
        data = self.__data_formatting(raw_data)

        loaded_bars = []

        # put a bar into parser
        for row in data:
            bar_ = parse_bar(row)
            if bar_ is not None and (self.getBarFilter() is None or self.getBarFilter().includeBar(bar_)):
                loaded_bars.append(bar_)
        
        # register bars list with product name
        self.addBarsFromSequence(prod_code, loaded_bars)
    
    def addBarsFromSequence(self, instrument, bars):
        super().addBarsFromSequence(instrument, bars)

    def __duplicate_bar(self, ret_data:list, prev_bar: dict, current_bar: dict):
        """
        duplicate bar if the bar didn't updated for a given interval
        eg. given bar interval: 5 seconds
            previous bar: 2022-08-02 09:00:05
            next bar    : 2022-08-02 09:00:20
        This function will create the missing bars like:
            2022-08-02 09:00:10

            2022-08-02 09:00:15
        """
        diff = current_bar['T'] - prev_bar['T']
        diff_sec = int(diff.total_seconds())
        nums_bar_created = int((diff_sec / self.get_interval()) - 1)

        for count in range(nums_bar_created):
            offset = self.get_interval() * (count + 1)
            copy_bar = prev_bar.copy()
            copy_bar['T'] = copy_bar['T'] + timedelta(seconds=offset)
            ret_data.append(copy_bar)

    # format the sp price data, making it suitalbe for pyalgotrade BarFeed to receive
    def __data_formatting(self, raw_data):
        if isinstance(raw_data, str):
            raise RuntimeError('Data should be in json format.')
        else:
            ret_data = []
            data_deque = deque(raw_data)
            prev = None

            while data_deque:
                bar_data = data_deque.popleft()
                del bar_data['TO']
                del bar_data['CO']
                time_stamp = bar_data['T']
                bar_data['T'] = datetime.fromtimestamp(int(time_stamp))

                if prev:
                    self.__duplicate_bar(ret_data, prev, bar_data)

                prev = bar_data
                ret_data.append(bar_data)
            
            for row in ret_data:
                # row['T'] is a datetime object, strftime makes it become a string in self-defined format
                row['T'] = row['T'].strftime(self.__date_time_format)
                # print(row)

            return ret_data
    
    # it asks for other function to creates basicBars for each product
    # given a parser and asking add_bars_from_json to fetch data from SP price server and create bars
    def __create_bars(self):
        for product in self.__prod_list:
            prod_code = product #.name # AttributeError: 'str' object has no attribute 'name'
            days_before = self.__days
            seconds = self.__bar_summary.input_time

            # The parser ensure the correctness of the datatime format
            row_parser = SpRowParser(
                self.__column_names, self.__date_time_format, self.getDailyBarTime(), self.getFrequency(),
                self.__timezone, self.__bar_class
            )
            
            self.add_bars_from_json(prod_code, days_before, seconds, row_parser)

        if row_parser.barsHaveAdjClose():
            self.__have_adj_close = True
        elif self.__have_adj_close:
            raise Exception("Previous bars had adjusted close and these ones don't have.")

    def __create_frequency(self, bar_summary: BarSummary):
        """
            bar_summary defines the time interval for each bar in seconds.
            return the input time by user and frequency object from pyalgotrade.
            note: bar summary of the products should be the same.
        """
        bar_summary_dict = bar_summary.dict()
        input_time = bar_summary_dict['input_time']
        for key, val in list(bar_summary_dict.items()):
            if val and key in frequency_dict:
                frequency = frequency_dict[key]
                return (frequency, input_time / frequency) 

    # def data_formatting(self, raw_data):
    #     temp_data1 = raw_data.split(':')
    #     temp_data2 = temp_data1[4].split(',0\r\n') # Remove 0 at end of each line
    #     temp_data3 = map(lambda bar: bar.split(','), temp_data2) # Format data for processing in the future
    #     data = list(temp_data3)
    #     data.pop()
    #     for i, bar in enumerate(data):
    #         ori_date = bar.pop()
    #         date_time = datetime.fromtimestamp(int(ori_date))
    #         # str_date = date_time.strftime('%Y-%m-%d %H:%M:%S')
    #         str_date = date_time.strftime(self.__dateTimeFormat)
    #         bar.insert(0, str_date)
    #     return data


# The parser originally fits to addBarsFromCSV from pyalgotrade library
# but we no longer use csv as data input.
class SpRowParser(csvfeed.RowParser):
    """
    The parser originally fits to addBarsFromCSV from pyalgotrade library.
    So, it contains getDelimiter().
    But we no longer use csv as data input. Now, it directly add bars from sp price json.
    """
    def __init__(self, column_names, datetime_format, daily_bar_time, frequency, timezone, bar_class=bar.BasicBar):
        self.__dateTimeFormat = datetime_format
        self.__dailyBarTime = daily_bar_time
        self.__frequency = frequency
        self.__timezone = timezone
        self.__haveAdjClose = False
        self.__barClass = bar_class

        self.__dateTimeColName = column_names["datetime"]
        self.__openColName = column_names["open"]
        self.__highColName = column_names["high"]
        self.__lowColName = column_names["low"]
        self.__closeColName = column_names["close"]
        self.__volumeColName = column_names["volume"]
        self.__columnNames = column_names

    def _parseDate(self, dateString):
        ret = datetime.strptime(dateString, self.__dateTimeFormat)
        
        if self.__dailyBarTime is not None:
            ret = datetime.combine(ret, self.__dailyBarTime)
        # Localize the datetime if a timezone was given.
        if self.__timezone:
            ret = dt.localize(ret, self.__timezone)
        return ret

    def barsHaveAdjClose(self):
        return self.__haveAdjClose

    def getFieldNames(self):
        # It is expected for the first row to have the field names.
        return self.__columnNames

    def getDelimiter(self):
        return ","

    def parseBar(self, RowDict):
        dateTime = self._parseDate(RowDict[self.__dateTimeColName])
        open_ = float(RowDict[self.__openColName])
        high = float(RowDict[self.__highColName])
        low = float(RowDict[self.__lowColName])
        close = float(RowDict[self.__closeColName])
        volume = float(RowDict[self.__volumeColName])
        adjClose = None

        # Process extra columns.
        extra = {}
        for k, v in six.iteritems(RowDict):
            if k not in self.__columnNames.values():
                extra[k] = csvutils.float_or_string(v)

        return self.__barClass(
            dateTime, open_, high, low, close, volume, adjClose, self.__frequency, extra=extra
        )