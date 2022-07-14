from pyalgotrade.barfeed import csvfeed
import pandas as pd
import spbar


class SpFeed(csvfeed.GenericBarFeed):
    def __init__(self, frequency=spbar.Frequency.SECOND, timezone=None, maxLen=None):
            if frequency not in [spbar.Frequency.SECOND, spbar.Frequency.MINUTE, spbar.Frequency.HOUR, spbar.Frequency.DAILY]:
                raise Exception("Invalid frequency")

            super(SpFeed, self).__init__(frequency, timezone, maxLen)


    def addBarsFromJson(self, instrument, data):

            # Load the json-formated data
            loadedBars = []
            myData = pd.read_json(data, orient = 'index')
            newData = myData.to_csv(index = False)
            for bar_ in newData:
                loadedBars.append(bar_)

            return self.addBarsFromSequence(instrument, loadedBars)