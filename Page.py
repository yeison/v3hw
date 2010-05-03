import sqlite3
from Entropy import *

imageList = ['bird.J.bmp', 'bird.N.bmp', 'bird.r.R.bmp', 'bird.W.bmp',
             'school1.J.bmp', 'school1.N.bmp', 'school1.Q.bmp','school1.T.bmp',
             'bass.B.bmp', 'bass.J.bmp', 'bass.N.bmp', 'bass.Q.bmp', 
             'old_lady.C.bmp', 'old_lady.J.bmp', 'old_lady.N.bmp', 'old_lady.Q.bmp']

conn = sqlite3.connect('page.db')
c = conn.cursor()
c.execute('''drop table if exists graphics''')
c.execute('''
create table if not exists graphics (Image, rpc, bpc, nc, rprc, bprc, nrc, rank)
''')

def imgize(image):
    shelfName = 'shelves/' + image + '.shelf'

    i = '''<h4>''' + image + '''</h4><img src='images/''' + image + ''''></img>
<h5>H(1) = %s</h5>
<h5>H(2) = %s</h5>
<h5>H(3) = %s</h5>
<h5>H(4) = %s</h5>''' % (entropy(0, shelfName), entropy(1, shelfName), entropy(2, shelfName), entropy(3, shelfName))
    rpc = '''<img src='graphs/rpc-''' + image + ''''></img>'''
    bpc = '''<img src='graphs/bpc-''' + image + ''''></img>'''
    nc = '''<img src='graphs/nc-''' + image + ''''></img>'''
    rprc = '''<img src='graphs/rprc-''' + image + ''''></img>'''
    bprc = '''<img src='graphs/bprc-''' + image + ''''></img>'''
    nrc = '''<img src='graphs/nrc-''' + image + ''''></img>'''
    rank = '''<img src='graphs/rank-''' + image + ''''></img>'''

    return i, rpc, bpc, nc, bprc, rprc, nrc, rank

for i in range(len(imageList)):
    c.execute('insert into graphics values(?,?,?,?,?,?,?,?)', imgize(imageList[i]))

conn.commit()
conn.close()


