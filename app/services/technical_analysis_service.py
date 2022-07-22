from core.config import SP_HOST_AND_PORT
from core.endpoints import DONETRADE
from collections import deque
from datetime import datetime
import pandas as pd
from schemas.technical_analysis_schemas import GetDoneTradeModel
from common.common_helper import CommonHelper

# ADMINACC = 'SPANSONLI'
# CLIENTACC = 'ANSONLI01'

ENDPOINT = SP_HOST_AND_PORT

class PnLService:
    __url = ENDPOINT + DONETRADE
    __df: pd.DataFrame
    accName: str
    col = ['date', 'TradePrice', 'Position', 'ProductCode', 'Balance', 'InstCode', 'ContractSize']

    def __init__(self, accName):
        self.accName = accName
        self.tradeNum = 0
        self.totalDoneContract = 0
        self._pnl = []
        self.__tradeRecords = []

    # get done trade record from SP API
    @classmethod
    def __get_done_trade(cls, request: GetDoneTradeModel):
        print(cls.__url, request)
        return CommonHelper.post_url(cls.__url, request)

    # prepare data for calculating PNL
    @staticmethod
    def __data_for_pnl(posList, priceList):
        # Creates double ended queue for buying and selling; converts poslist values accordingly
        buyRecordQueue = deque([{abs(record): priceList[i]} for i, record in enumerate(posList) if record < 0])
        sellRecordQueue = deque([{abs(record): priceList[i]} for i, record in enumerate(posList) if record > 0])
        # e.g. q = deque({1:2000}, {2:3000})

        for _ in range(len(buyRecordQueue)):
            buyTrade = buyRecordQueue.popleft() # Remove earliest buy from list
            # buyTrade is a dictionary; buyTrade.items() is a dict_items containing a list containing a tuple
            # num = list(buyTrade.items())[0] # num becomes a tuple
            num, price = list(buyTrade.items())[0] # num gets first value in tuple and removes it; price gets first value in new tuple
            for _ in range(num):
                buyRecordQueue.append(price) # Modifies list such that only prices remain in order of occurance 

        for _ in range(len(sellRecordQueue)):
            sellTrade = sellRecordQueue.popleft() # Remove earliest sell from list
            # sellTrade is a dictionary; sellTrade.items() is a dict_items containing a list containing a tuple
            # num = list(sellTrade.items())[0] # num becomes a tuple
            num, price = list(sellTrade.items())[0] # num gets first value in tuple and removes it; price gets first value in new tuple
            for _ in range(num):
                sellRecordQueue.append(price) # Modifies list such that only prices remain in order of occurance 

        result = {
            'buyRecordQueue': buyRecordQueue,
            'buyTradeNum': len(buyRecordQueue),
            'sellRecordQueue': sellRecordQueue,
            'sellTradeNum': len(sellRecordQueue)
        }

        return result

    # calculate PNL for a product
    @staticmethod
    def __cal_pnl(tradeRecordObj): # tradeRecordObj from __dat_for_pnl function; buyRecordQueue and sellRecordQueue are deque
        pnlQueue = deque()
        returnQueue = deque()
        buyRecordQueue: deque = tradeRecordObj['buyRecordQueue'] 
        sellRecordQueue: deque = tradeRecordObj['sellRecordQueue'] 
        buyTradeNum: int = tradeRecordObj['buyTradeNum']
        sellTradeNum: int = tradeRecordObj['sellTradeNum']
        
        pnlNum = min(buyTradeNum, sellTradeNum)

        # for _ in range(pnlNum): 
        #     sell_price = sellRecordQueue.popleft()
        #     buy_price = buyRecordQueue.popleft()
        #     pnl = sell_price - buy_price
        #     pnlQueue.append(
        #         tuple(pnl, sell_price)
        #     )

        # return (pnlQueue, pnlNum)
        for _ in range(pnlNum): # To ensure that there are corresponding pairs for pnlQueue values
            sell_price = sellRecordQueue.popleft()
            buy_price = buyRecordQueue.popleft()
            pnl = sell_price - buy_price

            pnlQueue.append(pnl) 
            returnQueue.append(pnl / buy_price) # Return = Profit/(Initial investment)
        return (pnlQueue, pnlNum, returnQueue)
    
    @staticmethod
    def __returns(prodCode): # Return of product overall; Profit = Return * Initial investment value 
        #  Refers to net return (retSubperiod = (sellvalue - buyvalue - depositedcash)/buyvalue = )
        # return returns # Returns for each product
        pass

    # create two separated deque for positive and negative value
    @staticmethod
    def __separation(queue: deque):
        positive = deque([val for val in queue if val > 0])
        negative = deque([val for val in queue if val < 0])
        return (positive, negative)

    # # data for pandas dataframe feeding
    # @staticmethod
    # def __ret_separation(pnlQueue: deque):
    #     positiveRet = deque([ret for ret in pnlQueue if ret > 0])
    #     negativeRet = deque([ret for ret in pnlQueue if ret < 0])
    #     return (positiveRet, negativeRet)

    def __create_data_for_feed(self, sortedDoneTradeRecords):

        for trade in sortedDoneTradeRecords: # For each trade in the trading records
            date = datetime.fromtimestamp(trade['timeStamp']).strftime('%Y-%m-%d %H:%M:%S')
            ordTotalQty: int
            tradePrice = trade['tradePrice']
            prodCode = trade['prodCode']
            instCode = trade['instCode']
            contractSize = trade['tsContractSize']
            if trade["buySell"]=="B": ordTotalQty = -trade['ordTotalQty']
            elif trade["buySell"]=="S": ordTotalQty = trade['ordTotalQty']
            self.tradeNum = self.tradeNum + 1

            self.__tradeRecords.append([date, tradePrice, ordTotalQty, prodCode, ordTotalQty, instCode, contractSize])

    # pandas dataframe feed
    def __data_feed(self):
        df = pd.DataFrame(data=self.__tradeRecords, columns=PnLService.col)
        df.date = pd.to_datetime(df.date)
        self.__df = df.groupby(['ProductCode', 'date', 'Position', 'Balance', 'InstCode', 'ContractSize'])[['TradePrice']].mean()

    def __create_separated_df(self): # Groups together trades with same product code
        l=[]
        index_count=1
        index_check=self.__df.index[0][0]

        for i in range(len(self.__df.index)):
            if index_check != self.__df.index[i][0]:
                index_check = self.__df.index[i][0]
                index_count = index_count + 1
                l += [i]
            else:
                continue

        l_mod = [0] + l + [len(self.__df)]
        dataframeList = [self.__df.iloc[l_mod[n]:l_mod[n + 1]] for n in range(len(l_mod) - 1)]

        return dataframeList

    # get profit and loss for each done-traded product
    def get_pnl(self, request: GetDoneTradeModel):

        # write performance analysis code below
        pnl = []
        res = self.__get_done_trade(request) # Admin access right required, cannot target own admin account
        try:
            allTradeData = res['data']['recordData'] 
            # {'result_code': -52020004, 'result_msg': 'API USER NO ACCESS RIGHT', 'timestamp': 1657697876}
            # {'result_code': 40011, 'result_msg': 'ACCESS UNAUTHORIZED', 'timestamp': 1657701648}
            # None
        except:
            raise SystemExit("The system currently cannot be accessed. Try testing again later.")
        # sortedDoneTradeRecords = sorted(
        #     res['data']['recordData'], 
        #     key=lambda trade: (trade['prodCode'], trade['timeStamp'])
        # )

        # create csv file for data feed
        self.__create_data_for_feed(allTradeData)
        # data feed
        self.__data_feed()
        #create separated dataframe
        dataframeList = self.__create_separated_df()

        for dataframe in dataframeList: # For product in dataframe for specific product code
            dataframe.reset_index(level=['Position', 'Balance','InstCode','ContractSize'], inplace=True)

            indexList = dataframe.index.to_list()
            prodCode = indexList[0][0]
            
            posList = dataframe['Position'].values.tolist()
            priceList = dataframe['TradePrice'].values.tolist()

            tradeRecordObj = self.__data_for_pnl(posList, priceList)
            # pnlQueue, pnlNum = self.__cal_pnl(tradeRecordObj) # A tuple of a deque containing pnls and the length of the deque
            pnlQueue, pnlNum, returnQueue = self.__cal_pnl(tradeRecordObj)
            positivePnl, negativePnl = self.__separation(pnlQueue) # deque for positive and negative pnl respectively
            positiveRet, negativeRet = self.__separation(returnQueue)

            for code in dataframe['InstCode']: #get one instcode and one contractsize instead of all
                InstCode = code
                break 
            for size in dataframe['ContractSize']:
                contractSize = size
                break
            pnl.append(
                {
                    InstCode: # e.g. HSI
                    {
                    'prodCode': prodCode, # Code of product (e.g. HSIM2)
                    'contractSize': contractSize,
                    'num': pnlNum,
                    "pnl": pnlQueue,
                    'positivePnl': positivePnl,
                    'negativePnl': negativePnl,
                    'returns': returnQueue,
                    'positiveRet': positiveRet,
                    'negativeRet': negativeRet
                    }
                    # e.g.
                    # 'HSI': {prodCode: 'HSIM2', ...},
                    # 'HSI': {prodCode: 'HSIZ2' ,....}
                }
            )
            self.totalDoneContract = self.totalDoneContract + pnlNum
            
        self._pnl = {   #combine the market code values in one list if the instcode is the same
            k: [d.get(k) for d in pnl if k in d]
            for k in set().union(*pnl)
        }
        # e.g.
        # pnl = {
        #     'HSI': [
        #         {prodCode: 'HSIM2', ...}, 
        #         {prodCode: 'HSIZ2' ,....}, ...
        #     ],
        #     'YMU': [...]
        # }
        return self._pnl
        #return json.dumps({'msg': 'from done trade analysis.'})
        
        # if exception rasied,
        # raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=errMsg)