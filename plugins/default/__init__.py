# Display the default fallback displays for when there is nothing
# else to show, consisting of just the AOSC logo and a clock
################################################################################
import datetime as dt
import os

htmlpfx = 'file://'+os.path.abspath(os.path.dirname(__file__))
lowPriorityParams = {
    'enabled'     : True,
    'updateFreq'  : dt.timedelta(hours=24),
    'dispDuration': dt.timedelta(hours=1),
    'priority'    : (0,1.0)
}

class Header:
    def getParams(self):
        params = lowPriorityParams
        params['location']      = 'header'
        return params

    def getPage(self):
        html = htmlpfx+'/header.html'
        return html


class Footer:
    def getParams(self):
        params = {}
        params = lowPriorityParams
        params['location']      = 'footer'
        return params

    def getPage(self):
        html = htmlpfx+'/footer.html'
        return html

# The half class will be added to the list twice, 
#  so that it can show up in both halves if there is 
#  absolutely nothing to display (should never happen though, hopefully)
class Half:
    def getParams(self):
        params = {}
        params = lowPriorityParams
        params['location']      = 'half'
        return params

    def getPage(self):
        html = htmlpfx+'/half.html'
        return html


## the list of all available displays in this plugin,
## as required by the plugin loader
displays = [Header, Footer, Half, Half]
