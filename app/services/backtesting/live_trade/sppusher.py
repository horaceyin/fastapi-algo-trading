import json    
class Event(object):
    def __init__(self, eventDict, dataIsJSON):
        self.__eventDict = eventDict
        self.__data = eventDict.get("data") #get sp ticker price as event
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