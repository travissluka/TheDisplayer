# Display the default fallback displays for when there is nothing
# else to show, consisting of just the AOSC logo and a clock
################################################################################
import displayplugin as dp

import datetime as dt
import os, shutil


lowPriorityParams = {
    'enabled'     : True,
    'updateFreq'  : dt.timedelta(hours=1),
    'dispDuration': dt.timedelta(hours=1),
    'priority'    : (0,1.0)
}


## code to get the ip address
import socket
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

            
class Header:
    def update(self):
        tmpdir = dp.gentmpdir()       
        params = {}
        params = lowPriorityParams
        params['location']      = 'header'
        params['html']          = "file://"+tmpdir+'/header.html'

        ## get the current IP address, and insert
        ## the last 2 numbers into the HTML file
        addr = get_ip_address().split('.')
        ip1=addr[0]
        ip2=addr[1]
        with open("header.html",'r') as fin:
            with open(tmpdir+"/header.html",'w') as fout:
                for line in fin:
                    line=line.replace("#IP1#",ip1)
                    line=line.replace("#IP2#",ip2)
                    fout.write(line)
        ## copy other files needed
        shutil.copy('style.css',tmpdir)
        shutil.copy('aosc_logo.png',tmpdir)
        
        return params
    


    
class Footer:
    def update(self):
        tmpdir = dp.gentmpdir()
        
        params = {}
        params = lowPriorityParams
        params['location']      = 'footer'
        params['html']          = "file://"+tmpdir+'/footer.html'

        ## get the current IP address, and insert
        ## the last 2 numbers into the HTML file
        addr = get_ip_address().split('.')
        ip3=addr[2]
        ip4=addr[3]
        with open("footer.html",'r') as fin:
            with open(tmpdir+"/footer.html",'w') as fout:
                for line in fin:
                    line=line.replace("#IP3#",ip3)
                    line=line.replace("#IP4#",ip4)
                    fout.write(line)
        ## copy other files needed
        shutil.copy('style.css',tmpdir)
        shutil.copy('CMNS_aosc_logo1.png',tmpdir)
        
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
