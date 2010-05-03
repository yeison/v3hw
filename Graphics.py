import rpy2.robjects as ro
from rpy2.robjects.packages import importr
import shelve
from opencv.highgui import *
import sys

imageName =  sys.argv[1]
shelfName = 'shelves/' + imageName + '.shelf'
dir = 'graphs/'

shelf = shelve.open(shelfName, 'r')
histoBlue = shelf['blue']
histoRed = shelf['red']
histoRedI = shelf['redI']
histoBlueI = shelf['blueI']
histoRank = shelf['rank']

graphics = importr('graphics')
stats = importr('stats')
spline = stats.spline
grdevices = importr('grDevices')
newGraph = grdevices.png
devOff = grdevices.dev_off
barNames = list((i*5 for i in range(256/5)))

##### Contrast Graphs #########
newGraph(file=dir + 'bpc-' + imageName)
graphics.barplot(ro.IntVector(tuple(histoBlue)),\
                     main='Histogram of Blue-Pixel Contrast',\
                     xlab='Contrast',\
                     ylab = 'Frequency x 1000',\
                     names = ro.IntVector(list(i*5 for i in range(256/5))),\
                     space = 0, \
                     col = 'blue', \
                     xlim = ro.IntVector((0,20)))
devOff()

newGraph(file=dir + 'rpc-' + imageName)
graphics.barplot(ro.IntVector(tuple(histoRed)),\
                     main='Histogram of Red-Pixel Contrast',\
                     xlab='Contrast',\
                     ylab = 'Frequency',\
                     names = ro.IntVector(list(i*5 for i in range(256/5))),\
                     space = 0, \
                     col = 'red', \
                     xlim = ro.IntVector((0,20)))
devOff()

newGraph(file=dir + 'nc-' + imageName)
graphics.plot(spline(ro.IntVector(tuple(histoBlue))),\
                  main = 'Normalized Histogram of Contrasts',
                  ylab='Frequency',\
                  xlab='Contrast x 5',\
                  col = 'blue',\
                  xlim = ro.IntVector((0,20)),\
                  type = 'l')
graphics.points(spline(ro.IntVector(tuple(histoRed))),\
                    col='red',\
                    type='l')
devOff()

##### Relative Contrast Graphs #############xs
newGraph(file=dir + 'bprc-' + imageName)
graphics.barplot(ro.IntVector(tuple(histoBlueI)),\
                     main='Histogram of Blue-Pixel Relative Contrast',\
                     xlab='Relative Contrast',\
                     ylab = 'Frequency x 1000',\
                     names = ro.IntVector(list(i*5 for i in range((256*256)/5))),\
                     space = 0, \
                     col = 'blue', \
                     xlim = ro.IntVector((0,50)))
devOff()

newGraph(file=dir + 'rprc-' + imageName)
graphics.barplot(ro.IntVector(tuple(histoRedI)),\
                     main='Histogram of Red-Pixel Relative Contrast',\
                     xlab='Relative Contrast',\
                     ylab = 'Frequency',\
                     names = ro.IntVector(list(i*5 for i in range((256*256)/5))),\
                     space = 0, \
                     col = 'red', \
                     xlim = ro.IntVector((0,50)))
devOff()

newGraph(file=dir + 'nrc-' + imageName)
graphics.plot(spline(ro.IntVector(tuple(histoBlueI))),\
                  main = 'Normalized Histogram of Relative Contrasts',
                  ylab='Frequency',\
                  xlab='Relative Contrast',\
                  col = 'blue',\
                  xlim = ro.IntVector((0,50)),\
                  type = 'l')
graphics.points(spline(ro.IntVector(tuple(histoRedI))),\
                    col='red',\
                    type='l')
devOff()

######## Rank Graph #############
newGraph(file=dir + 'rank-' + imageName)
graphics.barplot(ro.IntVector(tuple(histoRank)),\
                     main = 'Histogram of Ranks',\
                     names = ro.IntVector((1, 2, 3, 4)),\
                     xlab = 'Rank',\
                     ylab = 'Frequency',\
                     space=0)
devOff()
