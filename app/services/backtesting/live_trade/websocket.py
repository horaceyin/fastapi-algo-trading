import datetime
import json
import pyalgotrade.logger
from six.moves import queue

from pyalgotrade.websocket import pusher
from pyalgotrade.websocket import client


logger = pyalgotrade.logger.getLogger()#prodname
def get_current_datetime():
    return datetime.datetime.now()

class Event(object):
    def __init__(self, eventDict, dataIsJSON):
        self.__eventDict = eventDict
        self.__data = eventDict.get("data")
        if self.__data is not None and dataIsJSON:
            self.__data = json.loads(self.__data)

    def __str__(self):
        return str(self.__eventDict)

    def getDict(self):
        return self.__eventDict

    def getData(self):
        return self.__data

    def getType(self):
        return self.__eventDict.get("event")



class Trade(pusher.Event):
    """A trade event."""

    def __init__(self, dateTime, eventDict):
        super(Trade, self).__init__(eventDict, True)
        self.__dateTime = dateTime

    def getDateTime(self):
        """Returns the :class:`datetime.datetime` when this event was received."""
        return self.__dateTime

    def getId(self):
        """Returns the trade id."""
        return self.getData()["id"]

    def getPrice(self):
        """Returns the trade price."""
        return self.getData()["price"]

    def getAmount(self):
        """Returns the trade amount."""
        return self.getData()["amount"]

    def isBuy(self):
        """Returns True if the trade was a buy."""
        return self.getData()["type"] == 0

    def isSell(self):
        """Returns True if the trade was a sell."""
        return self.getData()["type"] == 1


class OrderBookUpdate(pusher.Event):
    """An order book update event."""

    def __init__(self, dateTime, eventDict):
        super(OrderBookUpdate, self).__init__(eventDict, True)
        self.__dateTime = dateTime

    def getDateTime(self):
        """Returns the :class:`datetime.datetime` when this event was received."""
        return self.__dateTime

    def getBidPrices(self):
        """Returns a list with the top 20 bid prices."""
        return [float(bid[0]) for bid in self.getData()["bids"]]

    def getBidVolumes(self):
        """Returns a list with the top 20 bid volumes."""
        return [float(bid[1]) for bid in self.getData()["bids"]]

    def getAskPrices(self):
        """Returns a list with the top 20 ask prices."""
        return [float(ask[0]) for ask in self.getData()["asks"]]

    def getAskVolumes(self):
        """Returns a list with the top 20 ask volumes."""
        return [float(ask[1]) for ask in self.getData()["asks"]]


class WebSocketClient(pusher.WebSocketClient):#need to be defined.
    """
    This websocket client class is designed to be running in a separate thread and for that reason
    events are pushed into a queue.
    """

    PUSHER_APP_KEY = "de504dc5763aeef9ff52"

    class Event:
        TRADE = 1
        ORDER_BOOK_UPDATE = 2
        CONNECTED = 3
        DISCONNECTED = 4

    def __init__(self, queue):
        super(WebSocketClient, self).__init__(WebSocketClient.PUSHER_APP_KEY, 5)
        self.__queue = queue

    def onMessage(self, msg):
        # If we can't handle the message, forward it to Pusher WebSocketClient.
        event = msg.get("event")
        if event == "trade":
            self.onTrade(Trade(get_current_datetime(), msg))
        elif event == "data" and msg.get("channel") == "order_book":
            self.onOrderBookUpdate(OrderBookUpdate(get_current_datetime(), msg))
        else:
            super(WebSocketClient, self).onMessage(msg)



    def onClosed(self, code, reason):
        logger.info("Closed. Code: %s. Reason: %s." % (code, reason))
        self.__queue.put((WebSocketClient.Event.DISCONNECTED, None))

    def onDisconnectionDetected(self):
        logger.warning("Disconnection detected.")
        try:
            self.stopClient()
        except Exception as e:
            logger.error("Error stopping websocket client: %s." % (str(e)))
        self.__queue.put((WebSocketClient.Event.DISCONNECTED, None))


    def onConnectionEstablished(self, event):
        logger.info("Connection established.")
        self.__queue.put((WebSocketClient.Event.CONNECTED, None))

        channels = ["live_trades", "order_book"]
        logger.info("Subscribing to channels %s." % channels)
        for channel in channels:
            self.subscribeChannel(channel)

    def onError(self, event):
        logger.error("Error: %s" % (event))

    def onUnknownEvent(self, event):
        logger.warning("Unknown event: %s" % (event))

    ######################################################################
    # Bitstamp specific

    def onTrade(self, trade):
        self.__queue.put((WebSocketClient.Event.TRADE, trade))

    def onOrderBookUpdate(self, orderBookUpdate):
        self.__queue.put((WebSocketClient.Event.ORDER_BOOK_UPDATE, orderBookUpdate))


class WebSocketClientThread(client.WebSocketClientThreadBase):
    """
    This thread class is responsible for running a WebSocketClient.
    """

    def __init__(self):
        super(WebSocketClientThread, self).__init__()
        self.__queue = queue.Queue()
        self.__wsClient = None

    def getQueue(self):
        return self.__queue

    def run(self):
        super(WebSocketClientThread, self).run()

        # We create the WebSocketClient right in the thread, instead of doing so in the constructor,
        # because it has thread affinity.
        try:
            self.__wsClient = WebSocketClient(self.__queue)
            self.__wsClient.connect()
            self.__wsClient.startClient()
        except Exception:
            logger.exception("Failed to connect: %s")

    def stop(self):
        try:
            if self.__wsClient is not None:
                logger.info("Stopping websocket client.")
                self.__wsClient.stopClient()
        except Exception as e:
            logger.error("Error stopping websocket client: %s." % (str(e)))