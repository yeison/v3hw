import rpy2.robjects as ro
from rpy2.robjects.packages import importr
import shelve
from opencv.highgui import *

bird_BW = cvLoadImage("bird.J.bmp", CV_LOAD_IMAGE_GRAYSCALE)
bird = cvLoadImage("bird.J.bmp")

shelf = shelve.open('data', 'r')
histoBlue = shelf['blue']
histoRed = shelf['red']
histoRedI = shelf['redI']
histoBlueI = shelf['blueI']
histoRank = shelf['rank']

graphics = importr('graphics')
stats = importr('stats')
grdevices = importr('grDevices')
spline = stats.spline
newGraph = grdevices.dev_new
barNames = list((i*5 for i in range(256/5)))


graphics.barplot(ro.IntVector(tuple(histoBlue)),\
                     main='Histogram of Blue-Pixel Contrast',\
                     xlab='Contrast',\
                     ylab = 'Frequency x 1000',\
                     space = 0, \
                     col = 'blue', \
                     xlim = ro.IntVector((0,20)))
newGraph()
graphics.barplot(ro.IntVector(tuple(histoRed)),\
                     main='Histogram of Red-Pixel Contrast',\
                     xlab='Contrast',\
                     ylab = 'Frequency',\
                     space = 0, \
                     col = 'red', \
                     xlim = ro.IntVector((0,15)))


newGraph()
graphics.plot(spline(ro.IntVector(tuple(histoBlue))),\
                  main = 'Normalized Histogram of Pixel Contrasts',
                  ylab='Frequency',\
                  xlab='Contrast x 5',\
                  col = 'blue',\
                  xlim = ro.IntVector((0,16)),\
                  type = 'l')
graphics.points(spline(ro.IntVector(tuple(histoRed))),\
                    col='red',\
                    type='l')

#####
newGraph()
graphics.barplot(ro.IntVector(tuple(histoBlueI)),\
                     main='Histogram of Blue-Pixel Relative Contrast',\
                     xlab='Contrast',\
                     ylab = 'Frequency',\
                     space = 0, \
                     col = 'blue', \
                     xlim = ro.IntVector((0,400)))
newGraph()
graphics.barplot(ro.IntVector(tuple(histoRedI)),\
                     main='Histogram of Red-Pixel Relative Contrast',\
                     xlab='Contrast',\
                     ylab = 'Frequency',\
                     space = 0, \
                     col = 'red', \
                     xlim = ro.IntVector((0,400)))


newGraph()
graphics.plot(spline(ro.IntVector(tuple(histoBlueI))),\
                  main = 'Normalized Histogram of Pixel Relative Contrasts',
                  ylab='Frequency',\
                  xlab='Contrast',\
                  col = 'blue',\
                  xlim = ro.IntVector((0,400)),\
                  type = 'l')
graphics.points(spline(ro.IntVector(tuple(histoRed))),\
                    col='red',\
                    type='l')


newGraph()
graphics.barplot(ro.IntVector(tuple(histoRank)),\
                     space=0)

cvShowImage("Bird", bird_BW)
cvShowImage("Bird2", bird)
cvWaitKey()
