import urllib, json
import datetime as dt
import logging
log = logging.getLogger(__name__)

################################################################################
## REQUIRED parameters:
################################################################################

## data_url - e.g. "http://api.wunderground.com/api/3a5b82718926c103/conditions/q/MD/College_Park.json"

################################################################################

dataFreq = dt.timedelta(minutes=5)
iconpath='http://icons.wxbug.com/i/c/j/##.gif'



def readData():
    '''buffer the data so that we don't do reads too often'''
    ## is it time to get new data?
    ctime = dt.datetime.now()
    if ctime - readData.lastRead > dataFreq:
        log.debug('downloading new weather data')
        readData.lastRead = ctime
        response = urllib.urlopen(data_url)
        readData.data = json.loads(response.read())
    return readData.data
readData.data = None
readData.lastRead = dt.datetime.now() - dt.timedelta(days=3)

