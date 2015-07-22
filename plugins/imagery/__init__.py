import datetime as dt
import os
import urllib
from subprocess import call

htmlpfx = os.path.abspath(os.path.dirname(__file__))

globalParams = {
    'enabled'     : True,
    'updateFreq'  : dt.timedelta(minutes=20),
    'dispDuration': dt.timedelta(seconds=60),
    'priority'    : (1,1.0),
    'location'    : 'half',
}


class Imagery:
    def getParams(self):
        args = '--loop -d 25 "#0--1" -d300 "#-1" --colors=256 -O2' # -O2 --dither  --colors=256'
        params = globalParams.copy()

        filename="http://www.ssd.noaa.gov/goes/east/eaus/vis-animated.gif"
        urllib.URLopener().retrieve(filename, htmlpfx+"/visa.gif")
        call('gifsicle {0}/visa.gif {1} > {0}/vis.gif'.format(htmlpfx,args),shell=True)

        filename = "http://www.ssd.noaa.gov/goes/east/eaus/rb-animated.gif"
        urllib.URLopener().retrieve(filename, htmlpfx+"/rba.gif")
        call('gifsicle {0}/rba.gif {1} > {0}/rb.gif'.format(htmlpfx,args),shell=True)

        filename = "http://www.ssd.noaa.gov/goes/east/eaus/wv-animated.gif"
        urllib.URLopener().retrieve(filename, htmlpfx+"/wva.gif")
        call('gifsicle {0}/wva.gif {1} > {0}/wv.gif'.format(htmlpfx,args),shell=True)
        return params

    def getPage(self):
        return  'file://'+htmlpfx+'/imagery.html'


## the list of all available displays in this plugin,
## as required by the plugin loader
displays = [Imagery]
