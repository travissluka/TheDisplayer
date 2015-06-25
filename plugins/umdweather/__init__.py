import datetime as dt
import os

priority = 0,0
htmlpfx = 'file://'+os.path.abspath(os.path.dirname(__file__))
# NOTE: When creating these html pages,
#       if graphics are 4x3, they should be 1080x810, if 16x9, 1080x608

class FiveDay:
    def getParams(self):
        params = {}
        params['enabled']       = True
        params['updateFreq']    = dt.timedelta(seconds=60)
        params['dispDuration']  = dt.timedelta(seconds=60)
        params['priority']      = (1,1.0)
        params['location']      = 'half'
        return params
    def getPage(self):
        html = htmlpfx+'/FiveDay_UMDweather.html'
        return html

class SpecialFcst:
    def getParams(self):
        params = {}
        params['enabled']       = False
        params['updateFreq']    = dt.timedelta(seconds=60)
        params['dispDuration']  = dt.timedelta(seconds=60)
        params['priority']      = (2,2.0)
        params['location']      = 'half'

        ## TODO: Find a way to know if a special forecast graphic has been recently
        ##       created on weather.umd.edu
        ##       Example: Terps Gameday forecast, etc.

        #if status:
            #params['enabled'] = True

## the list of all available displays in this plugin,
## as required by the plugin loader
displays = [FiveDay]
