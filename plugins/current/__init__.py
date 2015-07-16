import datetime as dt
import os
import urllib
import current

htmlpfx = os.path.abspath(os.path.dirname(__file__))

globalParams = {
    'enabled'     : True,
    'updateFreq'  : dt.timedelta(minutes=10),
    'dispDuration': dt.timedelta(seconds=15),
    'priority'    : (1,2.0),
    'location'    : 'half',
}


class CSSWxBugDisplay:
    def getParams(self):
        params = globalParams.copy()
        ### NOTE INSERT CODE TO CREATE CURRENT DISPLAY THING HERE
        current.getCSSwxbug() # create the html file
        return params

    def getPage(self):
        return  'file://'+htmlpfx+'/currently.html'


## the list of all available displays in this plugin,
## as required by the plugin loader
displays = [CSSWxBugDisplay]
