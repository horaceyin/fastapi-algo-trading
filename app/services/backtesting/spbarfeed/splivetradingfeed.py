from pyalgotrade.barfeed import csvfeed
import pandas as pd
import spbar


class SpFeed(csvfeed.GenericBarFeed):
    def __init__(self, frequency=spbar.Frequency.SECOND, timezone=None, maxLen=None, loadedBars=[]):
        self.__loadedBars = loadedBars

        if frequency not in [spbar.Frequency.SECOND, spbar.Frequency.MINUTE, spbar.Frequency.HOUR, spbar.Frequency.DAILY]:
            raise Exception("Invalid frequency")

        super(SpFeed, self).__init__(frequency, timezone, maxLen)


    def addBarsFromJson(self, instrument, data):
            # Load the json-formated data
            if self.__loadedBars is not None:
                self.__loadedBars.append(None, data) #update the latest data instead of the whole data
                return self.addBarsFromSequence(instrument, self.__loadedBars)
            
            self.__loadedBars = []
            myData = pd.read_json(data, orient = 'index')
            newData = myData.to_csv(index = False)
            for bar_ in newData:
                self.__loadedBars.append(bar_)

            
            return self.addBarsFromSequence(instrument, self.__loadedBars)