from ImageAnalyzer import *
from opencv import cv
from opencv.highgui import *
import rpy2.robjects.lib.ggplot2 as ggplot2
import rpy2.robjects as ro
from rpy2.robjects.packages import importr


bird_BW = cvLoadImage("bird.J.bmp", CV_LOAD_IMAGE_GRAYSCALE)
bird = cvLoadImage("bird.J.bmp")

redPixels = []
bluePixels = []
histoRed = []
histoBlue = [0 for i in range(256)]
histoRedI = []
histoBlueI = []
width = range(scale, (bird.width-1) - scale)
height = range(scale, (bird.height-1) - scale)
last = (0, 0)
def maxContrast(scale):
    for i in width:
        for j in height:
            contrast = None
            for theta in range(1):
                contrast = max(contrast, abs(dofIA2(i, j, (theta*pi)/4 + pi/2, scale, bird_BW)))
                
                if bird[j][i][2] == 255:
                    redPixels.append((i,j))
                    histoRed.append(contrast)
                    histoRedI.append((100*contrast)/(bird_BW[j, i]+1))
            
                else:
                    bluePixels.append((i, j))
                    histoBlue.append(contrast)
                    histoBlueI.append((10*contrast)/(bird_BW[j, i]+1))

def traceRed(start, clength):
    contour = []
    contour.append(start)
    last = start
    current = start
    for j in range(clength):
        for i in range(8):
            d = 1
        #If i is odd theta is diagonal to the axes
            if(i%2):
                d = sqrt(2)
        #Instead of pi, use a truncated estimate to increase processing speed.
            theta = (i*3.1416)/4
        #Instead of hard coding x+1 y+1 etc.., I thought we should take
        #advantage of the fact that the grid is a euclidean plane
            x = int(current[0] + round(d*cos(theta)))
            print "x: %s" % x
            y = int(current[1] + round(d*sin(theta)))
            print "y: %s" % y
            if last != (x, y) and bird[y, x][2] == 255:
                last = current
                current = (x, y)
                contour.append(current)
                break
    return contour


        

maxContrast(3)
print traceRed(redPixels[0], len(redPixels))

graphics = importr('graphics')
graphics.hist(ro.IntVector(tuple(histoBlueI)), main='Histogram', xlab='Contrast')

grdevices = importr('grDevices')
grdevices.dev_new()

graphics.hist(ro.IntVector(tuple(histoBlueI)), main='Histogram', xlab='Contrast')



cvShowImage("Bird", bird_BW)
cvShowImage("Bird2", bird)
cvWaitKey()
