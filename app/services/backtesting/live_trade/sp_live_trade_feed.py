import datetime
import time

from six.moves import queue

from pyalgotrade import bar
from pyalgotrade import barfeed
from pyalgotrade import observer
QUEUE_TIMEOUT = 0.01
class SpLiveTradeFeed(barfeed.Basebarfeed):
    def __init__(self, maxLen=None):
        super(SpLiveTradeFeed, self).__init__(bar.Frequency.TRADE, maxLen)
        self.__barDicts = []
        self.registerInstrument("HSIU2")# The target product code
        self.__prevTradeDateTime = None
        self.__thread = None
        self.__wsClientConnected = False
        self.__enableReconnection = True
        self.__stopped = False
        self.__orderBookUpdateEvent = observer.Event()

    def buildWebSocketClientThread(self):
        return wsclient.WebSocketClientThread()