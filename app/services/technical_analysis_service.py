from csv import writer
from os import environ, path, remove
from dotenv import load_dotenv
from collections import deque
from datetime import datetime
import pandas as pd
from pandas.core.frame import DataFrame
from core.endpoints import DONETRADE
from schemas.technical_analysis_schemas import GetDoneTradeModel
from common.common_helper import CommonHelper

# ADMINACC = 'SPANSONLI'
# CLIENTACC = 'ANSONLI01'

load_dotenv
ENDPOINT = environ['SP_HOST_AND_PORT']

class TaService:
    __url = ENDPOINT + DONETRADE

    def __init__(self):
        pass

    @classmethod
    def __get_done_trade(cls, request: GetDoneTradeModel):
        return CommonHelper.post_url(cls.__url, request)
    
    @staticmethod
    def __create_csv_file(sortedDoneTradeRecords):
        count=0

        for trade in sortedDoneTradeRecords:
            count=count+1

        with open ("example.csv","w", newline="") as csvfile:
            myWriter = writer(csvfile)
            myWriter.writerow([0,0,0,0])
            for trade in sortedDoneTradeRecords:
                Date = datetime.fromtimestamp(trade['timeStamp']).strftime('%Y-%m-%d %H:%M:%S')
                if trade["buySell"]=="B":
                    myWriter.writerow([Date, trade["tradePrice"], -trade['ordTotalQty'], trade["prodCode"]])
                if trade["buySell"]=="S":
                    myWriter.writerow([Date, trade["tradePrice"], trade['ordTotalQty'], trade["prodCode"]])

    @staticmethod
    def __csv_feed():
        pdData = pd.read_csv('example.csv')
        df = pd.DataFrame(pdData.values,columns=['date','TradePrice','Position','ProductCode'])
        df['Balance'] = df['Position']
        df.date = pd.to_datetime(df.date)
        df2 = df.groupby(['ProductCode','date','Position', 'Balance'])[['TradePrice']].mean()

        if path.exists('example.csv'): remove('example.csv')

        return df2

    @staticmethod
    def __create_separated_df(dataframe: DataFrame):
        l=[]
        index_count=1
        index_check=dataframe.index[0][0]

        for i in range(len(dataframe.index)):
            if index_check != dataframe.index[i][0]:
                index_check = dataframe.index[i][0]
                index_count = index_count+1
                l += [i]
            else:
                continue

        l_mod = [0] + l + [len(dataframe)]
        dataframeList = [dataframe.iloc[l_mod[n]:l_mod[n+1]] for n in range(len(l_mod)-1)]

        return dataframeList

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

        return pnlQueue

    @classmethod
    def run_done_trade_analysis(cls, request: GetDoneTradeModel):

        # write performance analysis code below

        res = cls.__get_done_trade(request)
        sortedDoneTradeRecords = sorted(
            res['data']['recordData'], 
            key=lambda trade: (trade['prodCode'], trade['timeStamp'])
        )
        # create csv file for data feed
        cls.__create_csv_file(sortedDoneTradeRecords)
        
        # data feed
        dataframe = cls.__csv_feed()
        
        #create separated dataframe
        dataframeList = cls.__create_separated_df(dataframe)

        for product in dataframeList:
            product.reset_index(level=['Position', 'Balance'], inplace=True)

        for dataframe in dataframeList:
            indexList = dataframe.index.to_list()
            prodCode = indexList[0][0]
            posList = dataframe['Position'].values.tolist()
            priceList = dataframe['TradePrice'].values.tolist()
            tradeRecordObj = cls.__data_for_pnl(posList, priceList)
            pnlQueue = cls.__cal_pnl(tradeRecordObj)
            print("P/L for ({}): {}\n\n".format(prodCode, pnlQueue))

        return sortedDoneTradeRecords
        #return json.dumps({'msg': 'from done trade analysis.'})
        
        # if exception rasied,
        # raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=errMsg)
