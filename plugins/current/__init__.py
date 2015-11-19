import displayplugin as dp

import datetime as dt
import os, shutil
import urllib
#import current
import weather_underground as wu

import logging
log = logging.getLogger(__name__)




class CSSWxBugDisplay:
    def __init__(self):
        self.initialized = False
        
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


        ## get the data
        obs = wu.readData()['current_observation']
        def tl(key, val):
            return '<div class="obs_line"><div class="obs_lbl">'+key+'</div><div class="obs_text">'+val+'</div></div>'
        text = ''

        text += '<div class="temp">' +\
                '<div class="main_temp"><b>{:0.0f}</b><div class="F">&#8457</div></div>'.format(round(obs['temp_f'],0)) +\
                '<div class="feel_temp">Feels Like <b>{}</b> <div class="F">&#8457</div></div>'.format(obs['feelslike_f'])+\
                '</div>'

        text += '<div class="wind">' +\
                '<div class="wnd_circle">'+\
                  '<div id="circle"></div>' +\
                  '<div id="triangle"></div>' +\
                  '<div class="wnd_speed"><b>{:0.0f}</b></div>'.format(int(obs['wind_mph'])) +\
                  '<div class="wnd_mph">mph</div>'+\
                '</div>' +\
                '<div>Wind from <b>{}</b></div>'.format(obs['wind_dir']) +\
                '<div>Gusts <b>{}</b> mph </div>'.format(obs['wind_gust_mph']) +\
                '</div>'
        
        text += '<div class="otherInfo">' + \
               tl('Dew Point:','<b>{:0.0f}</b> F'.format(round(obs['dewpoint_f'],0))) +\
               tl('Humidity:','<b>{}</b>'.format(obs['relative_humidity'])) +\
               tl('Precip:','<b>{}</b> in'.format(obs['precip_today_in'])) +\
               '</div>'

        iconbase='http://icons.wxug.com/i/c/i/'
        iconbase='http://icons.wxug.com/i/c/v4/'
        iconext='.svg'
        text += '<div class="imageBox">' +\
                '<div class="wxImage"><img src="{}"></div>'.format(iconbase+obs['icon']+iconext) +\
                '<div class="wxCaption">{}</div>'.format(obs['weather']) +\
                '</div>'
        
        # text += obs['weather'] + '</br>'
        # text += '{:0.0f} F'.format(round(obs['temp_f'],0)) + '</br>'
        # text += 'Wind from {} {:0.0f} mph'.format(obs['wind_dir'], round(obs['wind_mph'],0)) + '</br>'
        # text += '{} mb'.format(obs['pressure_mb']) + '</br>'
        # text += '{} F'.format(obs['heat_index_f']) + '</br>'
        # text += '{} F'.format(obs['windchill_f']) + '</br>'        
        # text += '{} in.'.format(obs['precip_today_in']) + '</br>'
        
        # text += obs['observation_time'] + '</br>'

        ## write the file
        with open(htmlFile,'w') as html:
            html.write('''
<html>
  <head>
    <link rel="stylesheet" type="text/css" href="../common/style.css">
    <link rel="stylesheet" type="text/css" href="style.css">
  </head>
  <body>
    <div id="logo"><img src="http://icons.wxug.com/logos/PNG/wundergroundLogo_4c_horz.png"></div>
    <div id="InfoBox">
      <div class="title">'''+obs['display_location']['full']+'''</div>
      <div class="mainBox">'''+text+'''</div>      
      <div class="updated">'''+obs['observation_time']+'''</div>
    </div>
  </body>
</html>''')
        
#        current.getCSSwxbug(htmlFile) # create the html file

        ## link the other required files to the tmp directory
        shutil.copy('style.css', tmpdir)
        shutil.copy('background.png', tmpdir)

        # ##download the icons if we haven't already
        # if not self.initialized:
        #     log.debug('downloading WxBug icons...')
        #     current.downloadIcons(tmpdir)
        #     self.initialized = True
        #     log.debug('donw downloading WxBug icons')
        
        return params



## the list of all available displays in this plugin,
## as required by the plugin loader
def init():
    wu.data_url = data_url
    return [CSSWxBugDisplay() ]
