# ------------------------------------------------------------------------------
# display.py
#
# Main python logic for TheDisplayer, responsible for loading in the
# user defined configuration file, loading the display plugins, and
# periodically tell all of the plugins to update themselves. Schedules which
# displays will be shown when.
# ------------------------------------------------------------------------------

#Configure the system logging
import logging
logging.basicConfig(format='%(asctime)-13s [%(levelname)s] %(message)s')
log = logging.getLogger('')
log.setLevel(logging.INFO)
logging.addLevelName(logging.INFO, "\033[01;37mINFO \033[00m")
logging.addLevelName(logging.ERROR, "\033[01;31mERROR\033[00m")
logging.addLevelName(logging.WARN, "\033[01;33mWARN \033[00m")
logging.addLevelName(logging.CRITICAL, "\033[01;35mCRIT \033[00m")
#TODO, make this a rotating log file
#log.addHandler(logging.FileHandler('display.log'))

#-------------------------------------------------------------------

from glob import glob
import sys
import importlib


log.info("TheDisplayer - Display server for AOSC hallway monitors ")

#global variables
plugins = []


def init(configFile):
    log.debug("Running display.init()")
    global plugins

    # read in the configuration file
    log.info("Reading in main configuration file "+configFile)
    config = importlib.import_module(configFile)

    #get a list of the plugins available
    availPlugins=[]
    for p in glob('plugins/[a-zA-Z]*py'):
        mdBase = p.split('/')[-1].split('.')[0]
        availPlugins.append(mdBase)

    #load in the required display plugins
    plugins = []
    for cp in config.plugins:
        if cp not in availPlugins:
            log.error('Plugin: "{0}" specified in config is not available.'
              .format(cp))
        else:
            log.info('Plugin: "{0}" loaded'.format(cp))
            plugins.append(importlib.import_module('plugins.'+cp))


def update(idx):
    #TODO: write logic to determine scheduling

    return plugins[idx].getContent();
