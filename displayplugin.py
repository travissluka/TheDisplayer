## helper methods for plugins to use

import inspect
import os, shutil


## Get a temporary directory uniquely named for the calling class
## TODO: make unique directories if there are more than 1 instance of a class??
tmpbasedir = '/tmp/TheDisplayer'

def gentmpdir():
    
    frames = inspect.currentframe()
    callingclass = inspect.getargvalues(inspect.stack()[1][0])[3].get('self',None)

    if callingclass == None:
        caller = inspect.getargvalues(inspect.stack()[1][0])[3]['__path__'][0].split('/')[-1]
    else:
        caller = str(callingclass.__class__)
    dirname =  tmpbasedir +"/"+caller
    if not os.path.exists(dirname):        
        os.makedirs(dirname)
    return dirname
    
