# Display the default fallback displays for when there is nothing
# else to show, consisting of just the AOSC logo and a clock
################################################################################
import displayplugin as dp

import datetime as dt
import os


class Info:
    def update(self):
        params = {
            'enabled'     : True,
            'updateFreq'  : dt.timedelta(hours=24),
            'dispDuration': dt.timedelta(seconds=30),
            'priority'    : (1,0.2),
            'location'    : 'half',
            'html'        : "file://"+os.getcwd()+'/info.html'}
        return params



    
## the list of all available displays in this plugin,
## as required by the plugin loader
#displays = [Header, Footer, Half, Half]
displays = [Info()]
