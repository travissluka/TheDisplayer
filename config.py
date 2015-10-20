debug      = True
fullscreen = False

## Padding for use with full screen
## needed since EGLFS QT backend ignores the
##  overscan sizes given by linux  
pad_left   = 22
pad_top    = 38
pad_right  = 21
pad_bottom = 39

plugins = [
    'common',
    'default',
    
    'alerts',         ## NWS alert for specific location
#    'current',       ## realtime weatherbug data
    'imagery',        ## satellite imagery
#    'messages',    
    'nhc',            ## Hurricane charts for the atlantic
    'remote_loader',  ## remotely defined slideshow images
    'spc',            ## Storm prediction center outlooks
    'wpc',            ## weather prediction center synoptic charts
]


