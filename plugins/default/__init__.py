# Display the default fallback displays for when there is nothing
# else to show
import datetime as dt
import os

htmlpfx = 'file://'+os.path.abspath(os.path.dirname(__file__))

class Header:
    def getParams(self):
        params = {}
        params['enabled']       = True
        params['updateFreq']    = dt.timedelta(seconds=60)
        params['dispDuration']  = dt.timedelta(seconds=60)
        params['priority']      = (0,1.0)
        params['location']      = 'header'
        return params
    def getPage(self):
        html = htmlpfx+'/header.html'
        return html


class Footer:
    def getParams(self):
        params = {}
        params['enabled']       = True
        params['updateFreq']    = dt.timedelta(seconds=60)
        params['dispDuration']  = dt.timedelta(seconds=60)
        params['priority']      = (0,1.0)
        params['location']      = 'footer'
        return params
    def getPage(self):
        html = htmlpfx+'/footer.html'
        return html


## the list of all available displays in this plugin,
## as required by the plugin loader
displays = [Header, Footer]
