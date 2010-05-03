import os
from subprocess import *

imageList = ['bird.J.bmp', 'bird.N.bmp', 'bird.r.R.bmp', 'bird.W.bmp', 'school1.J.bmp', 'school1.N.bmp', 'school1.Q.bmp', 'school1.T.bmp', 'bass.B.bmp', 'bass.J.bmp', 'bass.N.bmp', 'bass.Q.bmp', 'old_lady.C.bmp', 'old_lady.J.bmp', 'old_lady.N.bmp', 'old_lady.L.bmp']

def crunch(imageList):
    for i in range(4, len(imageList)):
        p = Popen(['python', 'hw3.py', 'images/' + imageList[i]], stdout=PIPE)
        p.wait()
        print 'Process Finished'
        p1 = Popen(['python', 'Graphics.py', imageList[i]])

crunch(imageList)
