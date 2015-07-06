import datetime as dt
import os
import urllib

htmlpfx = os.path.abspath(os.path.dirname(__file__))

globalParams = {
    'enabled'     : True,
    'updateFreq'  : dt.timedelta(minutes=10),
    'dispDuration': dt.timedelta(seconds=60),
    'priority'    : (1,1.0),
    'location'    : 'half',
}


class Imagery:
    def getParams(self):
        params = globalParams.copy()
        filename = "http://www.ssd.noaa.gov/goes/east/eaus/vis.jpg"
        urllib.URLopener().retrieve(filename, htmlpfx+"/vis.jpg")
        filename = "http://www.ssd.noaa.gov/goes/east/eaus/rb.jpg"
        urllib.URLopener().retrieve(filename, htmlpfx+"/rb.jpg")
        filename = "http://www.ssd.noaa.gov/goes/east/eaus/wv.jpg"
        urllib.URLopener().retrieve(filename, htmlpfx+"/wv.jpg")

        return params

    def getPage(self):
        return  'file://'+htmlpfx+'/imagery.html'


## the list of all available displays in this plugin,
## as required by the plugin loader
displays = [Imagery]
