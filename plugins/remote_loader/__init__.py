# 
################################################################################
import displayplugin as dp
import logging
log = logging.getLogger(__name__)
import datetime as dt
import os
import urllib, urllib2
import imp
import shutil
import traceback,sys


################################################################################
## REQUIRED configuration
################################################################################

## 'remote_dirs' - an arry of html url locations

################################################################################

def init():
    classes = []
    
    for rd in remote_dirs:
        ## get the list of displays produced
        ## by this remote location
        log.info("reading: "+rd)
        try:
            dirConfigFile = rd+'/config.py'
            dirConfigTxt  = urllib2.urlopen(dirConfigFile).read()
            dirConfig={}
            exec dirConfigTxt in dirConfig
            assert ('displays' in dirConfig)
        except:
            err=traceback.format_exc(sys.exc_info())
            log.error("Error reading remote directory main configuration ("
                      +dirConfigFile+"):\n"
                      +err)
            continue

        ##load in each display
        for d in dirConfig['displays']:
            dispConfigFile = rd+'/'+str(d)+'/config.py'
            try:
                log.info("reading: "+dispConfigFile)
                dispConfigTxt = urllib2.urlopen(dispConfigFile).read()
                dispConfig={}
                exec dispConfigTxt in dispConfig
                del dispConfig['__builtins__']
                dispConfig['remote']=rd+'/'+d
            except:
                err=traceback.format_exc(sys.exc_info())
                log.error("Error reading remote plugin configuration ("
                          +dispConfigFile+")\n"+err)
                continue
                

            ## createa  new class for this display
            class NewClass(Slideshow) : pass
            NewClass.__name__ = d
            c2 = NewClass(dispConfig)
            classes.append(c2)

    ## done loading classes, return
    return classes


class Slideshow:
    def __init__(self,config):
        self.tmpdir=dp.gentmpdir()
        
        self.slideDuration = int(config['slideDuration'])
        self.loopCount     = int(config['loopCount'])
        self.slides        = config['slides']
        self.remote        = config['remote']
        self. params = {
            'enabled'     : True,
            'updateFreq'  : dt.timedelta(hours=12),
            'dispDuration': dt.timedelta(seconds=
                   len(self.slides)*self.loopCount*self.slideDuration),
            'priority'    : config['priority'],
            'location'    : 'half',
            'html'        : 'file:///'+self.tmpdir+'/index.html'
        }
        self.updated=False

        
    def update(self):
        if not self.updated:
            self.updated = True

            html = ''
            ## download the images
            dl=urllib.URLopener()
            for f in self.slides:
                img = self.remote+'/'+f
                dl.retrieve(img,self.tmpdir+'/'+f)
                html+='<div class="slide"><img src='+f+'></div>'

            ## generate the html file
            shutil.copy('style.css',self.tmpdir+'/')
            id=''
            if len(self.slides) > 1:
                id="slideshow"
                
            with open('index.html','r') as fin:
                with open(self.tmpdir+'/index.html','w') as fout:
                    line = fin.read()
                    line = line.replace("##ID##",id)
                    line = line.replace("##SLIDES##", html)
                    line = line.replace("##SLIDEDURATION##", str(self.slideDuration))
                    fout.write(line)

        return self.params

    
