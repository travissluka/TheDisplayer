debug      = True
fullscreen = False

## Padding for use with full screen
## needed since EGLFS QT backend ignores the
##  overscan sizes given by linux  
pad_left   = 0
pad_top    = 0
pad_right  = 0
pad_bottom = 0



## global parameters that multiple plugins use
########################################
config = {
    'latlon'         : (38.8967, 76.9275),
    'nws_office'     : 'LWX',
    }


## list of plugins, and their site specific configuration, to load in
########################################
plugins = {
    'common'  : {},
    'default' : {},

    ## NWS alert for specific location
    'alerts'  : {       
        'countycode' : 'MDC033'},
    
    ## realtime weather data
    'current' : {
        'data_url' : 'http://api.wunderground.com/api/3a5b82718926c103/conditions/q/MD/College_Park.json'},

    ## satellite imagery
    'imagery' : {},
    
    ## Hurricane charts for the atlantic
    'nhc' : {},

    ## remotely defined slideshow images
    'remote_loader': {
        'remote_dirs' : (
            'http://www.atmos.umd.edu/~tsluka/the_displayer/right',
        )},

    ## Storm prediction center outlooks
    'spc' : {},

    ## weather prediction center synoptic charts
    'wpc' : {},           
}
