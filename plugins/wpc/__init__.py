import displayplugin as dp

import datetime as dt
import os, shutil
import urllib
from subprocess import call



class WPCForecast:
    def update(self):
        tmpdir = dp.gentmpdir()
        
        params = {
            'enabled'     : True,
            'updateFreq'  : dt.timedelta(minutes=20),
            'dispDuration': dt.timedelta(seconds=60),
            'priority'    : (1,1.0),
            'location'    : 'half',
            'html'        : 'file://'+tmpdir+"/wpc.html"
        }

        ## copy required files to the temporary directory
        shutil.copy('style.css', tmpdir)
        shutil.copy('wpc.html', tmpdir)

        filename="http://www.wpc.ncep.noaa.gov/noaa/noaad1.gif"
        urllib.URLopener().retrieve(filename, tmpdir+"/day1.gif")
        
        filename="http://www.wpc.ncep.noaa.gov/noaa/noaad2.gif"
        urllib.URLopener().retrieve(filename, tmpdir+"/day2.gif")
        
        filename="http://www.wpc.ncep.noaa.gov/noaa/noaad3.gif"
        urllib.URLopener().retrieve(filename, tmpdir+"/day3.gif")

        return params


## the list of all available displays in this plugin,
## as required by the plugin loader
displays = [WPCForecast()]
