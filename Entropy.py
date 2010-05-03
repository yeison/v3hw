import shelve
from math import log, exp, pi
import sys

scale = 3

def f(p, theta, D):
    denom = (abs(D[p[0], p[1], theta + pi/2, scale]) + 1)
    return exp(-1/float(denom))

def P(i, theta, shelf):
    rankIds = shelf['rankIds']
    D = shelf['contrasts']
    ranks = shelf['rank']
    series = []
    if(ranks[i] == 0):
        return 1
    try:
        for j in range(ranks[i]):
            p_tau = rankIds[i][j][0]
            series.append(f(p_tau, theta, D)/\
                              (f(p_tau, 0, D) +\
                                   f(p_tau, pi/4, D) +\
                                   f(p_tau, pi/2, D) +\
                                   f(p_tau, (3*pi)/4, D)))
    except IndexError as e:
        print e
        print "\ti: %s" % i
        print "\trange: %s" % range(ranks[i])
        raise


    return (1/float(ranks[i]))*sum(series)
                      

def entropy(i, shelfName):
    shelf = shelve.open(shelfName, 'r')
    return -(P(i, 0, shelf)*log(P(i, 0, shelf)) +\
             P(i, pi/4, shelf )*log(P(i, pi/4, shelf)) +\
             P(i, pi/2, shelf)*log(P(i, pi/2, shelf)) +\
             P(i, (3*pi)/4, shelf)*log(P(i, (3*pi)/4, shelf)))


