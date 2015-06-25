################################################################################
## main.py
##
## Main python logic for TheDisplayer, responsible for loading in the
## user defined configuration file, loading the display plugins, and
## periodically tell all of the plugins to update themselves. Schedules which
## displays will be shown when.
##
################################################################################

## Configure the system logging
import logging
logging.basicConfig(format='%(asctime)-13s [%(levelname)s] %(message)s')
log = logging.getLogger('')
log.setLevel(logging.DEBUG)
logging.addLevelName(logging.INFO, "\033[01;37mINFO \033[00m")
logging.addLevelName(logging.ERROR, "\033[01;31mERROR\033[00m")
logging.addLevelName(logging.WARN, "\033[01;33mWARN \033[00m")
logging.addLevelName(logging.CRITICAL, "\033[01;35mCRIT \033[00m")
## TODO, make this a rotating log file
#log.addHandler(logging.FileHandler('display.log'))

##############################


from glob import glob
import sys
import importlib
import re
import datetime as dt


log.info("TheDisplayer - Display server for AOSC hallway monitors ")

## global variables
plugins = []    
config = None
currentDisplays = {
    'header':None,
    'footer':None,
    'half_1':None,
    'half_2':None}


def isFullscreen():
    return config.fullscreen


################################################################################


def getClassName(c):
    return '.'.join((c.__module__+'.'+c.__class__.__name__).split('.')[1:])



################################################################################


def init(configFile):
    log.debug("Running display.init()")

    global plugins
    global config

    ## read in the configuration file, remove the "py" at the
    ## end of the name if its there
    log.info('Reading in configuration file "{0}"'.format(configFile))    
    reg = re.search('(.*)(\.py)+', configFile)
    if reg:
        configFile = reg.group(1)
    config = importlib.import_module(configFile)

    ## get a list of the plugins available
    availPlugins=[]
    for p in glob('plugins/*/__init__.py'):
        mdBase = p.split('/')[1]
        availPlugins.append(mdBase)

    ## load in the required display plugins and get the list of display classes from
    ##  each (some plugins might provide more than one display)
    for cp in config.plugins:
        if cp not in availPlugins:
            log.error('Plugin: "{0}" specified in config is not available.'
              .format(cp))
        else:
            plugin     = importlib.import_module('plugins.'+cp)
            newClasses = [{'script':p()} for p in plugin.displays]
            for d in newClasses:
                log.info('Plugin loaded: {0}'.format(getClassName(d['script'])))
            plugins += newClasses

    ## initialize some of the fields for each display plugin
    for p in plugins:
        ## set the 'lastupdate" variable to some long time ago
        ##  so that the system will be forced to update it now
        p['lastUpdate'] = dt.datetime.now()
        p['lastStart']  = dt.datetime.now() - dt.timedelta(days=300) 
        p['lastEnd']    = dt.datetime.now() - dt.timedelta(days=300) 
        try:
            params = p['script'].getParams()
            for k in params:
                p[k] = params[k]
        except:
            log.error("Failure in 'getParams()' call to "+getClassName(p['script']))
      


################################################################################
################################################################################



def update():
 try:                           
#    log.debug("display.update()")
    global currentDisplays

    updates = {}

    # update the parameters for all plugins that are due for an updating
    for p in plugins:
        if (dt.datetime.now()-p['lastUpdate']) >= p['updateFreq']:
            log.debug("Calling getParams() for "+getClassName(p['script']))
            p['lastUpdate'] = dt.datetime.now()
            try:
                params = p['script'].getParams()
                for k in params:
                    p[k] = params[k]
            except Exception as inst:
                log.error("Failure in 'getParams()' call to "+getClassName(p['script']))

    #find a plugin to show for each display location
    for loc in currentDisplays:
        cur = currentDisplays[loc]
        if cur != None:
            cur['lastEnd'] = dt.datetime.now()
        newDisp = None

        # filter to have only enabled plugins available for given location
        avail = filter(
            lambda p: (loc.split('_')[0] in p['location'] and p['enabled']),
            plugins )       

        # filter out those already shown elsewhere, except for itself
        shownClasses = [p for p in filter(lambda p: p!=None, zip(*currentDisplays.items())[1])]
        avail = filter( lambda p: not p in shownClasses or p == cur, avail)

        # if there is nothing to possibly show (this shouldn't happen in 
        #  the production software), continue on to the next location
        if (len(avail) == 0 ):
            continue

        # select highest priority classes
        avail = sorted(avail, key=lambda p: -p['priority'][0])
        priority = avail[0]['priority'][0]
        avail = filter( lambda p: p['priority'][0] == priority, avail)

        # determine the weight for each class based on its relative priority and
        #  time since last shown
        weighted = [
            (a,(dt.datetime.now()-a['lastEnd']).total_seconds()*a['priority'][1])
            for a in avail]
        weighted = sorted(weighted, key= lambda p: -p[1])
        next = weighted[0][0]

        # set the display location to this new display if the previous one has expired
        # or if the new display is of a higher priority class
        if ( cur == None or 
             not cur['enabled'] or 
             next['priority'][0] > cur['priority'][0] or
             (dt.datetime.now()-cur['lastStart']) > cur['dispDuration'] ):
                newDisp = next
                      
        #update with the new page if we found one
        if newDisp:
            newDisp['lastEnd'] = dt.datetime.now()
            newDisp['lastStart'] = dt.datetime.now()
            currentDisplays[loc] = newDisp
            updates[loc] = newDisp['script'].getPage()
            log.debug('Setting "{0}" to {1}'.format(loc,getClassName(newDisp['script'])))

        #TODO, don't tell the c++ code to update if the page is the same and 
        # doesn't need refreshing
    return updates.items()


 except Exception as inst:
 #     #TODO: finer grained error handling, skip individual plugins that fail 
     log.critical("Error with python update()")
     log.critical(inst)
     return '';
