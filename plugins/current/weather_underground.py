import urllib, json
import datetime as dt
import logging
log = logging.getLogger(__name__)

url="http://api.wunderground.com/api/3a5b82718926c103/conditions/q/MD/College_Park.json"
dataFreq = dt.timedelta(minutes=5)



def readData():
    '''buffer the data so that we don't do reads too often'''
    ## is it time to get new data?
    ctime = dt.datetime.now()
    if ctime - readData.lastRead > dataFreq:
        log.debug('downloading new weather data')
        readData.lastRead = ctime
        response = urllib.urlopen(url)
        readData.data = json.loads(response.read())
    return readData.data
readData.data = None
readData.lastRead = dt.datetime.now() - dt.timedelta(days=3)


dat=readData()
obs = dat['current_observation']

print obs['display_location']['full']
print obs['observation_time']
print obs['weather']
print obs['wind_mph'], obs['wind_dir'], obs['wind_gust_mph']
print obs['pressure_mb'], obs['pressure_in']
print obs['dewpoint_f']
print obs['heat_index_f'], obs['windchill_f']
print obs['precip_today_in']
iconpath='http://icons.wxbug.com/i/c/j/##.gif'
print obs['icon']
