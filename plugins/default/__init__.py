# Display the default fallback displays for when there is nothing
# else to show, consisting of just the AOSC logo and a clock
################################################################################
import displayplugin as dp

import datetime as dt
import os


lowPriorityParams = {
    'enabled'     : True,
    'updateFreq'  : dt.timedelta(hours=24),
    'dispDuration': dt.timedelta(hours=1),
    'priority'    : (0,1.0)
}



class Header:
    def update(self):
        params = lowPriorityParams
        params['location']      = 'header'
        params['html']          = "file://"+os.getcwd()+'/header.html'
        return params


    
class Footer:
    def update(self):
        params = {}
        params = lowPriorityParams
        params['location']      = 'footer'
        params['html']          = "file://"+os.getcwd()+'/footer.html'        
        return params


    
# The half class will be added to the list twice, 
#  so that it can show up in both halves if there is 
#  absolutely nothing to display (should never happen though, hopefully)
class Half:
    def update(self):
        params = {}
        params = lowPriorityParams
        params['location']      = 'half'
        params['html']          = "file://"+os.getcwd()+'/half.html'        
        return params


## the list of all available displays in this plugin,
## as required by the plugin loader
#displays = [Header, Footer, Half, Half]
displays = [Header(), Footer(), Half(), Half()]
