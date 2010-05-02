from ImageAnalyzer import *
from opencv import cv
from opencv.highgui import *
import rpy2.robjects.lib.ggplot2 as ggplot2
import rpy2.robjects as ro
from rpy2.robjects.packages import importr


bird_BW = cvLoadImage("bird.J.bmp", CV_LOAD_IMAGE_GRAYSCALE)
bird = cvLoadImage("bird.J.bmp")

scale = 3
redPixels = []
bluePixels = []
histoRed = []
histoBlue = [0 for i in range(256)]
histoRedI = []
histoBlueI = []
width = range(scale, (bird.width-1) - scale)
height = range(scale, (bird.height-1) - scale)
for i in width:
    for j in height:
        contrast = None
        for theta in range(1):
            contrast = max(contrast, abs(dofIA2(i, j, (theta*pi)/4, scale, bird_BW)))

        if bird[j][i][2] == 255:
            redPixels.append((i,j))
            histoRed.append(contrast)
            histoRedI.append((100*contrast)/(bird_BW[j, i]+1))
            
        else:
            bluePixels.append((i, j))
            histoBlue.append(contrast)
            histoBlueI.append((10*contrast)/(bird_BW[j, i]+1))


graphics = importr('graphics')
graphics.hist(ro.IntVector(tuple(histoBlue)), main='Histogram of', xlab='Contrast')

grdevices = importr('grDevices')
grdevices.dev_new()

graphics.hist(ro.IntVector(tuple(histoRed)), main='Histogram of', xlab='Contrast')


cvShowImage("Bird", bird_BW)
cvShowImage("Bird2", bird)
cvWaitKey()
