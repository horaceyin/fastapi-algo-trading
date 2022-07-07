from os import environ
from dotenv import load_dotenv
from collections import deque
from datetime import datetime
import pandas as pd
from pandas.core.frame import DataFrame
from requests import request
from core.endpoints import DONETRADE
from schemas.technical_analysis_schemas import GetDoneTradeModel
from common.common_helper import CommonHelper

# ADMINACC = 'SPANSONLI'
# CLIENTACC = 'ANSONLI01'

load_dotenv
ENDPOINT = environ['SP_HOST_AND_PORT']

class PnLService:
    __url = ENDPOINT + DONETRADE
    __df: pd.DataFrame
    accName: str
    col = ['date', 'TradePrice', 'Position', 'ProductCode', 'Balance','InstCode']

    def __init__(self, accName):
        self.accName = accName
        self.tradeNum = 0
        self.totalDoneContract = 0
        self._pnl = []
        self.__tradeRecords = []

    @classmethod
    def __get_done_trade(cls, request: GetDoneTradeModel):
        return CommonHelper.post_url(cls.__url, request)

    @staticmethod
    def __data_for_pnl(posList, priceList):
        buyRecordQueue = deque([{abs(record): priceList[i]} for i, record in enumerate(posList) if record < 0])
        sellRecordQueue = deque([{abs(record): priceList[i]} for i, record in enumerate(posList) if record > 0])
        
        for _ in range(len(buyRecordQueue)):
            buyTrade = buyRecordQueue.popleft()
            num, price = list(buyTrade.items())[0]
            for _ in range(num):
                buyRecordQueue.append(price)

        for _ in range(len(sellRecordQueue)):
            sellTrade = sellRecordQueue.popleft()
            num, price = list(sellTrade.items())[0]
            for _ in range(num):
                sellRecordQueue.append(price)

        result = {
            'buyRecordQueue': buyRecordQueue,
            'buyTradeNum': len(buyRecordQueue),
            'sellRecordQueue': sellRecordQueue,
            'sellTradeNum': len(sellRecordQueue)
        }

        return result

    @staticmethod
    def __cal_pnl(tradeRecordObj):
        pnlQueue = deque()
        buyRecordQueue: deque = tradeRecordObj['buyRecordQueue']
        sellRecordQueue: deque = tradeRecordObj['sellRecordQueue']
        buyTradeNum: int = tradeRecordObj['buyTradeNum']
        sellTradeNum: int = tradeRecordObj['sellTradeNum']
        
        pnlNum = min(buyTradeNum, sellTradeNum)

        for _ in range(pnlNum): 
            pnlQueue.append(sellRecordQueue.popleft() - buyRecordQueue.popleft())

        return (pnlQueue, pnlNum)

    def __create_data_for_feed(self, sortedDoneTradeRecords):

        for trade in sortedDoneTradeRecords:
            date = datetime.fromtimestamp(trade['timeStamp']).strftime('%Y-%m-%d %H:%M:%S')
            ordTotalQty: int
            tradePrice = trade['tradePrice']
            prodCode = trade['prodCode']
            instCode = trade['instCode']
            if trade["buySell"]=="B": ordTotalQty = -trade['ordTotalQty']
            elif trade["buySell"]=="S": ordTotalQty = trade['ordTotalQty']
            self.tradeNum = self.tradeNum + 1

            self.__tradeRecords.append(
                [date, tradePrice, ordTotalQty, prodCode, ordTotalQty, instCode]
            )

    def __data_feed(self):
        df = pd.DataFrame(data=self.__tradeRecords, columns=PnLService.col)
        df.date = pd.to_datetime(df.date)
        self.__df = df.groupby(['ProductCode', 'date', 'Position', 'Balance', 'InstCode'])[['TradePrice']].mean()

    def __create_separated_df(self):
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

    def get_pnl(self, request: GetDoneTradeModel):

        # write performance analysis code below

        res = self.__get_done_trade(request)
        allTradeData = res['data']['recordData']

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

        for product in dataframeList:
            product.reset_index(level=['Position', 'Balance', 'InstCode'], inplace=True)

        for dataframe in dataframeList:
            indexList = dataframe.index.to_list()
            prodCode = indexList[0][0]
            posList = dataframe['Position'].values.tolist()
            priceList = dataframe['TradePrice'].values.tolist()
            for instcode in dataframe['InstCode']:
                InstCode = instcode
                break   
            tradeRecordObj = self.__data_for_pnl(posList, priceList)
            pnlQueue, pnlNum= self.__cal_pnl(tradeRecordObj)
            self._pnl.append(
                {
                    'prodCode': prodCode,
                    "pnl": pnlQueue,
                    'num': pnlNum,
                }
            )
            self.totalDoneContract = self.totalDoneContract + 1
            # print("P/L for ({}): {}\n\n".format(prodCode, pnlQueue))
        return self._pnl
        #return json.dumps({'msg': 'from done trade analysis.'})
        
        # if exception rasied,
        # raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=errMsg)