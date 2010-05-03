#!/usr/bin/env python
from ImageAnalyzer import *
from opencv import cv
from opencv.highgui import *
import sys

if len(sys.argv) > 1:
    imageName = sys.argv[1]
else:
    imageName = sys.argv[0]


bird_BW = cvLoadImage(imageName, CV_LOAD_IMAGE_GRAYSCALE)
bird = cvLoadImage(imageName)


def maxContrast(scale):
    redPixels = []
    bluePixels = []
    histoRed = [0 for i in range(256/5)]
    histoBlue = [0 for i in range(256/5)]
    histoRedI = [0 for i in range((256*256)/5)]
    histoBlueI = [0 for i in range((256*256)/5)]
    width = range(scale, (bird.width-1) - scale)
    height = range(scale, (bird.height-1) - scale)
    for i in width:
        for j in height:
            contrast = None
            for theta in range(4):
                new = abs(dofIA2(i, j, (theta*pi)/4 + pi/2, scale, bird_BW))
                contrast = max(contrast, new)
                
                if bird[j][i][2] == 255:
                    redPixels.append((i,j))
                    histoRed[contrast/5] += 1
                    histoRedI[((255*contrast)/(bird_BW[j, i]+1))/5] += 1
            
                else:
                    bluePixels.append((i, j))
                    histoBlue[contrast/5] += 1
                    histoBlueI[((255*contrast)/(bird_BW[j, i]+1))/5] += 1

    histoRed = normalize(histoRed)
    histoBlue = normalize(histoBlue)
    histoRedI = normalize(histoRedI)
    histoBlueI = normalize(histoBlueI)
    return dofIA2Hash, histoRed, histoBlue, histoRedI, histoBlueI, redPixels, bluePixels
            
def normalize(histo):
    sumHist = sum(histo)
    for i in range(len(histo)):
        if histo[i] > 0:
            histo[i] = 100*float(histo[i])/sumHist
        else:
            histo[i] = None
    return histo

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
ht, histoRed, histoBlue, histoRedI, histoBlueI, redPixels, bluePixels = maxContrast(scale)
trace = traceRed(redPixels[0], len(redPixels))
histoRank = [0, 0, 0, 0]
rankIds = [[], [], [], []]
for i in range(len(trace)):
    x, y = trace[i][0]
    rank = []
    for theta in range(4):
        rank.append(ht[x, y, (pi*theta)/4 + pi/2, scale])
    rank.sort()
    rank.reverse()
    for j in range(len(rank)):
        if(ht[x, y, (pi*trace[i][1])/4 + pi/2, scale] == rank[j]):
            rankIds[j].append(((x, y), (pi*trace[i][1])/4 + pi/2, scale))
            histoRank[j] += 1


import shelve
dbName = 'shelves/' + imageName.split('images/')[1] + '.shelf'
shelf = shelve.open(dbName, 'c')
shelf['blue'] = histoBlue
shelf['red'] = histoRed
shelf['blueI'] = histoBlueI
shelf['redI'] = histoRedI
shelf['rank'] = histoRank
shelf['contrasts'] = ht
shelf['rankIds'] = rankIds
shelf.close()
