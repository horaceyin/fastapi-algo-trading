from pyalgotrade.barfeed import csvfeed
from pyalgotrade.bar import Frequency
from pyalgotrade import bar
from pyalgotrade.utils import dt
from pyalgotrade.utils import csvutils
from services.backtesting.spbarfeed.sp_data import SpData
from schemas.backtesting.bar_summary_schemas import BarSummary
from datetime import datetime
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
        self.header = ['Date Time', 'Open', 'High', 'Low', 'Close', 'Volume']

        self.__timezone = timezone
        self.__have_adj_close = False
        self.__bar_class = bar.BasicBar
        self.__date_time_format = "%Y-%m-%d %H:%M:%S"
        self.__column_names = {
            "datetime": "T",
            "open": "O",
            "high": "H",
            "low": "L",
            "close": "C",
            "volume": "V",
            "adj_close": None
        }
        frequency, time = self.create_frequency(self.__bar_summary)
        super(SpBarFeed, self).__init__(frequency * time, maxLen = maxLen)
        self.create_bars()

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

    def add_bars_from_json(self, prod_code, days, seconds, row_parser, skip_malformed_bars=False):

        def parse_bar_skip_malformed(row):
            ret = None
            try:
                ret = row_parser.parseBar(row)
            except Exception:
                pass
            return ret

        if skip_malformed_bars:
            parse_bar = parse_bar_skip_malformed
        else:
            parse_bar = row_parser.parseBar
        
        # Load the json-formated data
        self.__sp_data.set_prod_code(prod_code)
        self.__sp_data.set_days_before(days)
        self.__sp_data.set_bar_seconds(seconds)

        raw_data = self.__sp_data.get_sp_data()

        data = self.data_formatting(raw_data)
        
        # json_data = pd.read_json(data, orient = 'index')
        # csv_data = json_data.to_csv(index = False, encoding='utf-8', columns=self.header)

        loaded_bars = []

        for row in data:
            bar_ = parse_bar(row)
            if bar_ is not None and (self.getBarFilter() is None or self.getBarFilter().includeBar(bar_)):
                loaded_bars.append(bar_)

        self.addBarsFromSequence(prod_code, loaded_bars)

    def data_formatting(self, raw_data):
        if isinstance(raw_data, str):
            raise RuntimeError('Data should be in json format.')
        else:
            for row_dict in raw_data:
                del row_dict['TO']
                del row_dict['CO']
                time_stamp = row_dict['T']
                date_time = datetime.fromtimestamp(int(time_stamp))
                row_dict['T'] = date_time.strftime(self.__date_time_format)
            return raw_data

    def create_bars(self):
        for product in self.__prod_list:
            prod_code = product #.name # AttributeError: 'str' object has no attribute 'name'
            days_before = self.__days
            seconds = self.__bar_summary.input_time

            row_parser = SpRowParser(
                self.__column_names, self.__date_time_format, self.getDailyBarTime(), self.getFrequency(),
                self.__timezone, self.__bar_class
            )
            
            self.add_bars_from_json(prod_code, days_before, seconds, row_parser)

        if row_parser.barsHaveAdjClose():
            self.__have_adj_close = True
        elif self.__have_adj_close:
            raise Exception("Previous bars had adjusted close and these ones don't have.")

    # all product have the same frequency
    def create_frequency(self, bar_summary: BarSummary):
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

class SpRowParser(csvfeed.RowParser):
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
