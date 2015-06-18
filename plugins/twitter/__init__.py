import datetime as dt
import os

htmlpfx = 'file://'+os.path.abspath(os.path.dirname(__file__))

class Twitter:
    def getParams(self):
        params = {}
        params['enabled']       = True
        params['updateFreq']    = dt.timedelta(seconds=60)
        params['dispDuration']  = dt.timedelta(seconds=60)
        params['priority']      = (0,1.0)
        params['location']      = 'half'
        return params
    def getPage(self):
        html = htmlpfx+'/twitter_aosc.html'
        return html

## the list of all available displays in this plugin,
## as required by the plugin loader
displays = [Twitter]
