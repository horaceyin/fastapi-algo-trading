# For analysers in sma_backtest_service

class DataInfo:
    def __init__():
        pass

    def construct_data(dataList):
        dateCol = []
        openCol = []
        highCol = []
        lowCol = []
        closeCol = []
        volumeCol = []
        for bar in dataList:
            dateCol.append(bar[0])
            openCol.append(bar[1])
            highCol.append(bar[2])
            lowCol.append(bar[3])
            closeCol.append(bar[4])
            volumeCol.append(bar[5])
        return (dateCol, openCol, highCol, lowCol, closeCol, volumeCol)

    def print_result(strat, retAnalyzer, sharpeRatioAnalyzer, drawDownAnalyzer, tradesAnalyzer):
        print("")
        print("Final portfolio value: $%.2f" % strat.getResult())
        print("Cumulative returns: %.4f %%" % (retAnalyzer.getCumulativeReturns()[-1] * 100))
        print("Sharpe ratio: %.2f" % (sharpeRatioAnalyzer.getSharpeRatio(0.05)))
        print("Max. drawdown: %.4f %%" % (drawDownAnalyzer.getMaxDrawDown() * 100))
        print("Longest drawdown duration: %s" % (drawDownAnalyzer.getLongestDrawDownDuration()))

        print("")
        print("Total trades: %d" % (tradesAnalyzer.getCount()))
        if tradesAnalyzer.getCount() > 0:
            profits = tradesAnalyzer.getAll()
            print("Avg. profit: $%2.2f" % (profits.mean()))
            print("Profits std. dev.: $%2.2f" % (profits.std()))
            print("Max. profit: $%2.2f" % (profits.max()))
            print("Min. profit: $%2.2f" % (profits.min()))

            returns = tradesAnalyzer.getAllReturns()
            print("Avg. return: %2.3f %%" % (returns.mean() * 100))
            print("Returns std. dev.: %2.3f %%" % (returns.std() * 100))
            print("Max. return: %2.3f %%" % (returns.max() * 100))
            print("Min. return: %2.3f %%" % (returns.min() * 100))

        print("")
        print("Profitable trades: %d" % (tradesAnalyzer.getProfitableCount()))

        if tradesAnalyzer.getProfitableCount() > 0:
            profits = tradesAnalyzer.getProfits()
            print("Avg. profit: $%2.2f" % (profits.mean()))
            print("Profits std. dev.: $%2.2f" % (profits.std()))
            print("Max. profit: $%2.2f" % (profits.max()))
            print("Min. profit: $%2.2f" % (profits.min()))
            returns = tradesAnalyzer.getPositiveReturns()
            print("Avg. return: %2.3f %%" % (returns.mean() * 100))
            print("Returns std. dev.: %2.3f %%" % (returns.std() * 100))
            print("Max. return: %2.3f %%" % (returns.max() * 100))
            print("Min. return: %2.3f %%" % (returns.min() * 100))

        print("")
        print("Unprofitable trades: %d" % (tradesAnalyzer.getUnprofitableCount()))

        if tradesAnalyzer.getUnprofitableCount() > 0:
            losses = tradesAnalyzer.getLosses()
            print("Avg. loss: $%2.2f" % (losses.mean()))
            print("Losses std. dev.: $%2.2f" % (losses.std()))
            print("Max. loss: $%2.2f" % (losses.min()))
            print("Min. loss: $%2.2f" % (losses.max()))
            returns = tradesAnalyzer.getNegativeReturns()
            print("Avg. return: %2.3f %%" % (returns.mean() * 100))
            print("Returns std. dev.: %2.3f %%" % (returns.std() * 100))
            print("Max. return: %2.3f %%" % (returns.max() * 100))
            print("Min. return: %2.3f %%" % (returns.min() * 100))

    # def prod_n_ccy(token2):
    #     produrl = ENDPOINT + PRODINFO
    #     productinfo = requests.post(produrl, 
    #     json = {
    #         "prodCode": self.__instrument, # Collects product code from sma_cross2, which collects from sma_strat2
    #         "sessionToken": token2,
    #         "dataRecordTotal": 100,
    #         "dataStartFromRecord": 0
    #     })
    #     recordDiction = json.loads(productinfo.text) 
    #     if recordDiction['result_code'] == 40011:
    #         recordsize = 0
    #         recordccy = "HKD"
    #     else:
    #         recordsize = recordDiction['data']['jsonData']['contractSize'] # Size of product
    #         recordccy = recordDiction['data']['jsonData']['ccy'] # Currency of product

    #     ccyrate = ENDPOINT + CCYRATES
    #     ccyratein = requests.post(ccyrate, 
    #     json = {
    #         "ccy": recordccy, # USD = 1
    #         "sessionToken": token2
    #     })
    #     ccyrateintext = json.loads(ccyratein.text) 
    #     if ccyrateintext['result_code'] == 40011:
    #         ccyrateinval = 1 
    #     else: 
    #         ccyrateinval = ccyrateintext['data']['recordData'][0]['rate'] # USD to recordccy
    #     ccyrateout = requests.post(ccyrate, 
    #     json = {
    #         "ccy": "HKD", 
    #         "sessionToken": token2
    #     })
    #     ccyrateouttext = json.loads(ccyrateout.text) 
    #     if ccyrateouttext['result_code'] == 40011:
    #         ccyrateoutval = 1 
    #     else: 
    #         ccyrateoutval = ccyrateouttext['data']['recordData'][0]['rate'] # USD to HKD
    #     ccyhkd = ccyrateoutval/ccyrateinval
    #     return recordsize, ccyhkd