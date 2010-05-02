#Yeison Rodriguez
#!/usr/bin/env python
from opencv import highgui, cv
from types import NoneType
from ImageAnalyzer import dofIA2, checkAngle
import sys

pi = 3.1416

class PixelArray(dict):
     def copyImage(self, image):
          width = range(self.scale-1, image.width-self.scale)
          height = range(self.scale-1, image.height-self.scale)
          for i in width:
               for j in height:
                    p = PixelNode(i, j, image[i, j])
                    self.addPixel(p)

     def getPixel(self, x, y):
          return self[x, y]


     def addPixel(self, pixel):
          self[pixel.x, pixel.y] = pixel
          self.list.append(pixel)
        
     def __init__(self, filename, scale):
          self.list = []
          self.scale = scale
          try:
               self.image = highgui.cvLoadImage(filename, highgui.CV_LOAD_IMAGE_GRAYSCALE)
            #Deal with borders/edges and performing analyses.
               self.n = (self.image.width - (scale + 2)) * (self.image.height - (scale + 2))
               if(type(self.image) == NoneType):
                    print >> sys.stderr, "  The filename provided does not exist."
                    sys.exit(1)
          except IndexError as e:
               print >> sys.stderr, "  Please provide the name of a local image."
               sys.exit(1)        
          dict.__init__(self)
          self.default = None
          self.copyImage(self.image)
          self.E = {}
        
     def __getitem__(self, key):
          try:
               return dict.__getitem__(self, key)
          except KeyError:
               print >> sys.stderr, "  The specified pixel is not accessible.  It might not exist"
               raise

#A PixelNode is defined by the pixel's location and its gray level.
class PixelNode(list):
     def __init__(self, x, y, grayValue):
          self.x = x
          self.y = y
          self.grayValue = grayValue

          for i in [-2, -1, 0, 1, 2, 3, 4, 5]:
               self.insert(i+2, AngleNode(self, i*pi/4))

          def __print__(self):
               print "x:%s  y:%s  gray:%s" % (self.x, self.y, self.grayValue)

          def __hash__(self):
               return hash(tuple(self))
    

class AngleNode:
    #Sets the contrast of a particular pixel-angle combination.
     def getContrast(self, pxl):
          T = 1
          self.contrast = T/(abs(dofIA2(pxl.x, pxl.y, angle, self.scale, self.image)) + 1)
          return self.contrast
     def findNeighbor(self, pixelArray):
          d = checkAngle(angle)
          nbrx = int(x + i*d*cos(theta))
          nbry = int(y + i*d*sin(theta))
          self.neighbor = pixelArray[nbrx, nbry]
          return self.neighbor

     def __init__(self, pixel, angle):
          self.parent = pixel
          self.angle = angle
          self.edgeCost = 100000
          self.pathCost = 100000
          self.contrast = None

