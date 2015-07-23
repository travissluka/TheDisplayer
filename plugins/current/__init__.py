import displayplugin as dp

import datetime as dt
import os, shutil
import urllib
import current



class CSSWxBugDisplay:
    def update(self):

        tmpdir = dp.gentmpdir()        
        htmlFile = tmpdir+'/currently.html'
        
        params = {
            'enabled'     : True,
            'updateFreq'  : dt.timedelta(minutes=10),
            'dispDuration': dt.timedelta(seconds=15),
            'priority'    : (1,3.0),
            'location'    : 'half',
            'html'        : 'file://'+htmlFile
        }       

        current.getCSSwxbug(htmlFile) # create the html file

        ## link the other required files to the tmp directory
        shutil.copy('style.css', tmpdir)
        shutil.copy('background.png', tmpdir)
        
        return params



## the list of all available displays in this plugin,
## as required by the plugin loader
displays = [CSSWxBugDisplay() ]
