import csv
import os
import json
import pandas as pd
from datetime import datetime
from requests import post
from os import environ
from dotenv import load_dotenv
from fastapi.encoders import jsonable_encoder
from schemas.technical_analysis_schemas import GetDoneTradeModel

load_dotenv()
ENDPOINT = environ['SP_END_POINT']

class TaService:
    def __init__(self):
        pass

    @staticmethod
    def run_done_trade_analysis(request: GetDoneTradeModel):
        myUrl = ENDPOINT + r'/apiCustomer/reporting/doneTrade'
        donetradedict = jsonable_encoder(request)
        res = post(url=myUrl,json=donetradedict)
        doneTradeDicts = res.json()
        doneTradeRecords=doneTradeDicts['data']['recordData']
        count=0
        for trade in doneTradeRecords:
            count=count+1
        with open ("example.csv","w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['0','0','0','0'])
            for trade in doneTradeRecords:
                Date = datetime.fromtimestamp(trade['timeStamp']).strftime('%Y-%m-%d %H:%M:%S')
                if trade["buySell"]=="B":
                    writer.writerow([Date, trade["tradePrice"],-trade['ordTotalQty'], trade["prodCode"]])
                if trade["buySell"]=="S":
                    writer.writerow([Date, trade["tradePrice"],trade['ordTotalQty'], trade["prodCode"]])
        data = pd.read_csv('example.csv')
        df = pd.DataFrame(data.values,columns=['date','TradePrice','Position','ProductCode'])
        df.date = pd.to_datetime(df.date)
        df2=df.groupby(['ProductCode','date','Position'])[['TradePrice']].mean()
        l=[]
        index_count=1
        index_check=df2.index[0][0]
        for i in range(len(df2.index)):
            if index_check!=df2.index[i][0]:
                index_check=df2.index[i][0]
                index_count=index_count+1
                l+=[i]
            else:
                continue
        l_mod = [0] + l + [len(df2)]
        list_of_dfs = [df2.iloc[l_mod[n]:l_mod[n+1]] for n in range(len(l_mod)-1)]
        Pnl=[]
        for i in range(index_count):
            _list=list_of_dfs[i].sort_values(['date'])
            new_list=_list.reset_index(level=['ProductCode','Position'])
            price_list=[]
            count=0
            position=0
            total=0
            for l in range(len(new_list)):
                position+=new_list['Position'][l]
                price_list.append(new_list["TradePrice"][l]*new_list['Position'][l])
                if len(price_list)==1:
                    Pnl.append('Nan')
                elif position==0:
                    if l!=0:
                        for element in range(len(price_list)):
                            total=total+price_list[element]
                        price_list.clear()
                        Pnl.append(total)
                        total=0
                    else:
                        Pnl.append('Nan')
                elif position<0 and count!=0 and len(price_list)!=1:
                    for element in range(len(price_list)):
                        total=total+price_list[element]
                    else:
                        total=total+price_list[element]-(new_list["TradePrice"][l])
                        Pnl.append(total)
                        price_list.clear()
                else:
                    Pnl.append('Nan')
                count=count+1
        df2['Pnl']=Pnl
        out = df2.to_json(orient='index')
        out=json.loads(out)
        file = 'example.csv'
        if(os.path.exists(file) and os.path.isfile(file)):
            os.remove(file)
        errMsg = ''
        return out
    