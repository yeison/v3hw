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

def maxContrast(scale):
    width = range(scale, (bird.width-1) - scale)
    height = range(scale, (bird.height-1) - scale)
    for i in width:
        for j in height:
            ranked = [0, 0, 0, 0]
            contrast = None
            for theta in range(4):
                new = abs(dofIA2(i, j, (theta*pi)/4 + pi/2, scale, bird_BW))
                contrast = max(contrast, new)
                
                if bird[j][i][2] == 255:
                    redPixels.append((i,j))
                    histoRed.append(contrast)
                    histoRedI.append((100*contrast)/(bird_BW[j, i]+1))
            
                else:
                    bluePixels.append((i, j))
                    histoBlue.append(contrast)
                    histoBlueI.append((10*contrast)/(bird_BW[j, i]+1))
    return dofIA2Hash
            

def traceRed(start, clength):
    contour = []
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
            #print "x: %s" % x
            y = int(current[1] + round(d*sin(theta)))
            #print "y: %s" % y
            if last != (x, y) and bird[y, x][2] == 255:
                last = current
                if i < 4:
                    angle = i
                else:
                    angle = i-4
                    
                contour.append((current, angle))
                current = (x, y)
                break
    return contour


scale = 3
ht = maxContrast(scale)
trace = traceRed(redPixels[0], len(redPixels))
histoRank = [0, 0, 0, 0]
for i in range(len(trace)):
    x, y = trace[i][0]
    rank = []
    for theta in range(4):
        rank.append(ht[x, y, (pi*theta)/4 + pi/2, scale])
    rank.sort()
    for j in range(len(rank)):
        print [x, y, (pi*trace[i][1])/4 + pi/2, scale]
        print rank[j]
        if(ht[x, y, (pi*trace[i][1])/4 + pi/2, scale] == rank[j]):
            "yes"
            histoRank[j] += 1
        
graphics = importr('graphics')
graphics.hist(ro.IntVector(tuple(histoBlueI)), main='Histogram', xlab='Contrast')

grdevices = importr('grDevices')
grdevices.dev_new()

graphics.hist(ro.IntVector(tuple(histoBlueI)), main='Histogram', xlab='Contrast')



cvShowImage("Bird", bird_BW)
cvShowImage("Bird2", bird)
cvWaitKey()
