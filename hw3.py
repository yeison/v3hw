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
histoBlue = []
histoRedI = []
histoBlueI = []
width = range(scale, (bird.width-1) - scale)
height = range(scale, (bird.height-1) - scale)
for i in width:
    for j in height:
        contrast = None
        for theta in range(1):
            contrast = max(contrast, abs(int(dofIA2(i, j, (theta*pi)/4, scale, bird_BW))))

        if bird[j][i][2] == 255:
            redPixels.append((i,j))
            histoRed.append(contrast)
            histoRedI.append((100*contrast)/(bird_BW[j, i]+1))
            
        else:
            bluePixels.append((i, j))
            histoBlue.append(contrast)
            histoBlueI.append((100*contrast)/(bird_BW[j, i]+1))


d = {'blue': ro.IntVector(histoBlueI), 'bin':ro.IntVector(range(256))}
dataf = ro.DataFrame(d)
gpb = ggplot2.ggplot(dataf)
hpb = gpb + \
    ggplot2.aes_string(y = 'blue', x='bin') + \
    ggplot2.geom_histogram()
hpb.plot()

grdevices = importr('grDevices')
grdevices.dev_new()

d = {'red': ro.IntVector(histoRedI)}
dataf = ro.DataFrame(d)
print dataf
gpr = ggplot2.ggplot(dataf)
hpr = gpr + \
    ggplot2.aes_string(x = 'red') + \
    ggplot2.stat_bin()
hpr.plot()


cvShowImage("Bird", bird_BW)
cvShowImage("Bird2", bird)
cvWaitKey()
