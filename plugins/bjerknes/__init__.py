import datetime as dt
import os

priority = 0,0
htmlpfx = 'file://'+os.path.abspath(os.path.dirname(__file__))

""" Display most recent visible satellite .gif """
class VisSat:
    def getParams(self):
        params = {}
        params['enabled']       = True
        params['updateFreq']    = dt.timedelta(seconds=60)
        params['dispDuration']  = dt.timedelta(seconds=60)
        params['priority']      = (1,1.0)
        params['location']      = 'half'
        return params
    def getPage(self):
        html = htmlpfx+'/sat_vis.html'
        return html

""" Display most recent regional radar .gif """
class RadarReg:
    def getParams(self):
        params = {}
        params['enabled']       = True
        params['updateFreq']    = dt.timedelta(seconds=60)
        params['dispDuration']  = dt.timedelta(seconds=60)
        params['priority']      = (1,1.0)
        params['location']      = 'half'
        return params
    def getPage(self):
        html = htmlpfx+'/radar_reg.html'
        return html

## the list of all available displays in this plugin,
## as required by the plugin loader
displays = [VisSat,RadarReg]
