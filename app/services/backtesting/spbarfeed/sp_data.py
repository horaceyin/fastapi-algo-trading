from common.common_helper import CommonHelper

# if data_mode = 2 (default), def data_formatting in spbarfeed/sp_bar_feed.py need to be changed
BASE_URL = 'https://chart3.spsystem.info/pserver/chartdata_query.php?data_mode=4&'

ERROR_MSG1 = '[]' # when data_mode = 2
ERROR_MSG2 = '19:-1:EMPTY RESULT!' # when data_mode = 4

class SpData():
    def __init__(self):
        self.__prod_code = None
        self.__days_before = None
        self.__bar_seconds = None

    def set_prod_code(self, prod_code):
        self.__prod_code = prod_code

    def set_days_before(self, days):
        self.__days_before = days

    def set_bar_seconds(self, seconds):
        self.__bar_seconds = seconds

    def get_sp_data(self):
        assert self.__prod_code, f'Product code is none, call set_prod_code()'
        assert self.__days_before, f'days is none, call set_days_before()'
        assert self.__bar_seconds, f'bar second is none, call set_bar_seconds()'
        
        URL = BASE_URL + f'days={self.__days_before}&second={self.__bar_seconds}&prod_code={self.__prod_code}'
        data = CommonHelper.get_url(URL)

        if len(data) == 0 or data == ERROR_MSG1 or data == ERROR_MSG2: 
            raise ValueError(f'The product name: "{self.__prod_code}" from SP price server does not found.')

        return data