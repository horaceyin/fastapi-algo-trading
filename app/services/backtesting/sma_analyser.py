# For analysers in sma_backtest_service

# from services.backtesting.sma_simple_cross import SMACrossOver
# from pyalgotrade.stratanalyzer import returns
# from pyalgotrade.stratanalyzer import sharpe
# from pyalgotrade.stratanalyzer import drawdown
# from pyalgotrade.stratanalyzer import trades

# strat = SMACrossOver(myFeed, self.__instrument, self.__smaPeriod)

# strat.getBroker().setCash(self.__startcash) # Set new value of portfolio

# retAnalyzer = returns.Returns()
# strat.attachAnalyzer(retAnalyzer)

# sharpeRatioAnalyzer = sharpe.SharpeRatio()
# strat.attachAnalyzer(sharpeRatioAnalyzer)

# drawDownAnalyzer = drawdown.DrawDown()
# strat.attachAnalyzer(drawDownAnalyzer)

# tradesAnalyzer = trades.Trades()
# strat.attachAnalyzer(tradesAnalyzer)

# def print_result(strat, retAnalyzer, sharpeRatioAnalyzer, drawDownAnalyzer, tradesAnalyzer):
#     print("")
#     print("Final portfolio value: $%.2f" % strat.getResult())
#     print("Cumulative returns: %.4f %%" % (retAnalyzer.getCumulativeReturns()[-1] * 100))
#     print("Sharpe ratio: %.2f" % (sharpeRatioAnalyzer.getSharpeRatio(0.05)))
#     print("Max. drawdown: %.4f %%" % (drawDownAnalyzer.getMaxDrawDown() * 100))
#     print("Longest drawdown duration: %s" % (drawDownAnalyzer.getLongestDrawDownDuration()))

#     print("")
#     print("Total trades: %d" % (tradesAnalyzer.getCount()))
#     if tradesAnalyzer.getCount() > 0:
#         profits = tradesAnalyzer.getAll()
#         print("Avg. profit: $%2.2f" % (profits.mean()))
#         print("Profits std. dev.: $%2.2f" % (profits.std()))
#         print("Max. profit: $%2.2f" % (profits.max()))
#         print("Min. profit: $%2.2f" % (profits.min()))

#         returns = tradesAnalyzer.getAllReturns()
#         print("Avg. return: %2.3f %%" % (returns.mean() * 100))
#         print("Returns std. dev.: %2.3f %%" % (returns.std() * 100))
#         print("Max. return: %2.3f %%" % (returns.max() * 100))
#         print("Min. return: %2.3f %%" % (returns.min() * 100))

#     print("")
#     print("Profitable trades: %d" % (tradesAnalyzer.getProfitableCount()))

#     if tradesAnalyzer.getProfitableCount() > 0:
#         profits = tradesAnalyzer.getProfits()
#         print("Avg. profit: $%2.2f" % (profits.mean()))
#         print("Profits std. dev.: $%2.2f" % (profits.std()))
#         print("Max. profit: $%2.2f" % (profits.max()))
#         print("Min. profit: $%2.2f" % (profits.min()))
#         returns = tradesAnalyzer.getPositiveReturns()
#         print("Avg. return: %2.3f %%" % (returns.mean() * 100))
#         print("Returns std. dev.: %2.3f %%" % (returns.std() * 100))
#         print("Max. return: %2.3f %%" % (returns.max() * 100))
#         print("Min. return: %2.3f %%" % (returns.min() * 100))

#     print("")
#     print("Unprofitable trades: %d" % (tradesAnalyzer.getUnprofitableCount()))

#     if tradesAnalyzer.getUnprofitableCount() > 0:
#         losses = tradesAnalyzer.getLosses()
#         print("Avg. loss: $%2.2f" % (losses.mean()))
#         print("Losses std. dev.: $%2.2f" % (losses.std()))
#         print("Max. loss: $%2.2f" % (losses.min()))
#         print("Min. loss: $%2.2f" % (losses.max()))
#         returns = tradesAnalyzer.getNegativeReturns()
#         print("Avg. return: %2.3f %%" % (returns.mean() * 100))
#         print("Returns std. dev.: %2.3f %%" % (returns.std() * 100))
#         print("Max. return: %2.3f %%" % (returns.max() * 100))
#         print("Min. return: %2.3f %%" % (returns.min() * 100))

