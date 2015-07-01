import datetime as dt
import os

htmlpfx = 'file://'+os.path.abspath(os.path.dirname(__file__))

globalParams = {
    'enabled'     : True,
    'updateFreq'  : dt.timedelta(minutes=10),
    'dispDuration': dt.timedelta(seconds=60),
    'priority'    : (1,1.0),
    'location'    : 'half',
}


class Visible:
    def getParams(self):
        global globalParams
        return globalParams

    def getPage(self):
        return  htmlpfx+'/visible.html'


class IR:
    def getParams(self):
        global globalParams
        return globalParams

    def getPage(self):
        return  htmlpfx+'/ir.html'

class WV:
    def getParams(self):
        global globalParams
        return globalParams

    def getPage(self):
        return  htmlpfx+'/wv.html'


## the list of all available displays in this plugin,
## as required by the plugin loader
displays = [Visible, IR, WV]
