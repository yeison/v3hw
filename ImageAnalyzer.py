#  ImageAnalyzer.py  
#
#  Created by Yeison Rodriguez on 3/1/10.
#  Copyright (c) 2010 __Yeison Rodriguez__. All rights reserved.
#
from opencv import highgui, cv
from math import sin, cos, pi, sqrt, floor
from types import NoneType

#Determines if the angle is diagonal with respect to the x or y axes.
def checkAngle(theta):
    if((theta*2)/pi == int((theta*2)/pi)):
        return 1
    else:
        return sqrt(2) 

#Checks if the lookup table has this value already computed.
def getFromLUT(LUT, x, y, theta, scale):
    try:
        value = LUT[x, y, theta, scale]
    except KeyError as e:
        return None
    return value

iA1Hash = {}
def intensityAccum1(x, y, theta, scale, image):
#Pixel value array
    iA1ValueExists = getFromLUT(iA1Hash, x, y, theta, scale)
    if iA1ValueExists:
        return iA1ValueExists
    pxArray = []
    d = checkAngle(theta)
    for i in range(scale):
        target_x = int(x + i*d*cos(theta))
        target_y = int(y + i*d*sin(theta))
        #The if statements below checks for a case on the edges where
        #rounding to an integer steps outside of the image dimentions.
        if(target_x >= image.width):
            target_x = int(x + floor(i*d*cos(theta)))
        if(target_y >= image.height):
            target_y = int(y + floor(i*d*sin(theta)))
        #print "x: %s" %  int(x + i*cos(theta))
        pxArray.append(image[target_y, target_x])
    iA1Value = sum(pxArray)/scale
    iA1Hash[x, y, theta, scale] = iA1Value
    return iA1Value
#Shorten the function name
iA1 = intensityAccum1

iA2Hash = {}
def intensityAccum2(x, y, theta, s, image):
    valueExists = getFromLUT(iA2Hash, x, y, theta, s)
    if valueExists:
        return valueExists
    d = checkAngle(theta)
    if(d == 1): #If theta is along a straight line.
        term1 = iA1(x, y, theta, s, image)
        term2 = iA1(x+d*cos(theta), y+d*sin(theta), theta, s, image)
        term3 = iA1(x-d*sin(theta), y+d*cos(theta), theta, s, image)
        term4 = iA1(x+d*sin(theta), y-d*cos(theta), theta, s, image)
        ia2 = (term1 + term2 + term3 + term4)/4
        iA2Hash[x, y, theta, s] = ia2
        return ia2
    else:       #If theta is along a diagonal.
        term1 = iA1(x, y, theta, s, image)
        term2 = iA1(x+d*cos(theta), y+d*sin(theta), theta, s, image)
        term3 = iA1(x, y+d*sin(theta), theta, s, image)
        term4 = iA1(x+d*cos(theta), y, theta, s, image)
        ia2 = (term1 + term2 + term3 + term4)/4
        iA2Hash[x, y, theta, s] = ia2
        return ia2
#Shorten function name
iA2 = intensityAccum2

#Derivative of iA2 along angle theta.
dofIA2Hash = {}
def dofIA2(x, y, theta, s, image):
    valueExists = getFromLUT(dofIA2Hash, x, y, theta, s)
    if valueExists:
        return valueExists
    d = checkAngle(theta)
    deriv = iA2(x, y, theta, s, image) - iA2(x-d*cos(theta), y-d*sin(theta), pi + theta, s, image)
    dofIA2Hash[x, y, theta, s] = deriv
    return deriv
