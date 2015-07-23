import inspect
import displayplugin as dp

import shutil, os
## copy required common files need by web pages into the web tmp directory

os.chdir(os.path.dirname(__file__))

dirname = dp.gentmpdir()
shutil.copy('jquery.min.js', dirname)
shutil.copy('style.css', dirname)

displays = []        
