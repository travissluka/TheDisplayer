import datetime as dt
import os

class Sample1:
    def getParams(self):
        params = {}
        params['enabled']       = True
        params['updateFreq']    = dt.timedelta(minutes=2)
        params['dispDuration']  = dt.timedelta(seconds=60)
        params['priority']      = (0,1.0)
        params['location']      = 'half'
        return params

    def getPage(self):
        html = 'http://www.atmos.umd.edu'
        return html


class Sample2:
    def getParams(self):
        params = {}
        params['enabled']       = True
        params['updateFreq']    = dt.timedelta(minutes=2)
        params['dispDuration']  = dt.timedelta(seconds=60)
        params['priority']      = (0,1.0)
        params['location']      = 'half'
        return params

    def getPage(self):
        html = 'http://www.weather.gov'
        return html

class Sample3:
    def getParams(self):
        params = {}
        params['enabled']       = True
        params['updateFreq']    = dt.timedelta(minutes=2)
        params['dispDuration']  = dt.timedelta(seconds=60)
        params['priority']      = (0,1.0)
        params['location']      = 'half'
        return params

    def getPage(self):
        html = 'http://www.weather.com'
        return html

class Sample4:
    def getParams(self):
        params = {}
        params['enabled']       = True
        params['updateFreq']    = dt.timedelta(minutes=2)
        params['dispDuration']  = dt.timedelta(seconds=60)
        params['priority']      = (0,1.0)
        params['location']      = 'footer'
        return params

    def getPage(self):
        html = 'http://travissluka.com'
        return html


## the list of all available displays in this plugin,
## as required by the plugin loader
displays = [Sample1, Sample2, Sample3, Sample4]
