################################################################################
## Support library to parse the shape files from the SPC to determine what
##  the outlook levels are for our location for the various days and categories
################################################################################
import feedparser
import urllib2
import datetime as dt
import time
import re
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

## configurables

feedurl = "http://www.spc.noaa.gov/products/spcacrss.xml"

## the size, in degrees, of the box around our central location
## to use when testing if our location is inside a outlook region
locSize = (.1,.1)

#####################################################

def getOutlooksForLoc(center=None):
    ## build a box around our given location that we will test against
    if center:
        loc = Polygon([
            (center[0]+locSize[0], center[1]+locSize[1]),
            (center[0]+locSize[0], center[1]-locSize[1]),
            (center[0]-locSize[0], center[1]-locSize[1]),
            (center[0]-locSize[0], center[1]+locSize[1])])

    ## Get information about the outlooks for each lead day
    ####################################
    retVal = {}    
    for day in [1,2,3]: #don't deal with 48 right now (4-8 day), as the images behave diferently
        retVal[day] = {}

        ## get the shapes file from the intertubes
        dy=str(day)
        if day < 10:
            dy = 'y'+dy
        shapeFileUrl = "http://weather.noaa.gov/pub/data/raw/wu/wuus{0:02d}.kwns.pts.d{1}.txt".format(day,dy)
        shapeFile = urllib2.urlopen(shapeFileUrl).read()
        
        ## split the file up into the individual outlook categories, and get the shapes for each
        ##  warning level within the outlook category
        categories = re.findall(r'\.\.\. (.+?) \.\.\.(.+?)\&\&',shapeFile,flags=re.DOTALL)
        for category in categories:
            ## parse out a list of coords
            words = category[1].split()
            
            ## ignore if its empty
            if len(words) == 0:
                continue

            ## get the shape types and coordinates
            shapes = []
            newCoords = []
            idx = 0
            lbl = None
            while idx < len(words):
                ## see if it is a label, and not a coord
                if not re.match('^[0-9]{8}$',words[idx]):
                    if lbl:
                        shapes.append((lbl,newCoords))
                    lbl = words[idx]
                    newCoords=[]
                else:
                    ## convert the text into a coord
                    c = words[idx]
                    coord = (float(c[0:2]+"."+c[2:4]),float(c[4:6]+"."+c[6:8]))
                    ## lon >= 100 have the first 1 missing, add it back in
                    if coord[1] < 10:
                        coord = (coord[0], coord[1]+100)
                    newCoords.append(coord)
                idx += 1
            if lbl:
                shapes.append((lbl,newCoords))

            ## test to see which shapes we are inside
            shapesIn = []
            for s in shapes:
                if s[0] not in shapesIn:  ## only include levels once
                    if not center or Polygon(s[1]).intersects(loc):
                        shapesIn.append(s[0])

            retVal[day][category[0]] = shapesIn

    return retVal
                
