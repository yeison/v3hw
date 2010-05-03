import shelve
from math import pi, log, exp

shelf = shelve.open('data', 'r')
rankIds = shelf['rankIds']
D = shelf['contrasts']
ranks = shelf['rank']


def f(p, theta):
    denom = (abs(D[p[0], p[1], theta + pi/2, scale]) + 1)
    return exp(-1/float(denom))

def P(i, theta):
    series = []
    for j in range(ranks[i]):
        p_tau = rankIds[i][j][0]
        series.append(f(p_tau, theta)/\
                          (f(p_tau, 0) +\
                               f(p_tau, pi/4) +\
                               f(p_tau, pi/2) +\
                               f(p_tau, (3*pi)/4)))

    return (1/float(ranks[i]))*sum(series)
                      

def entropy(i):
    return -(P(i, 0)*log(P(i, 0)) +\
             P(i, pi/4)*log(P(i, pi/4)) +\
             P(i, pi/2)*log(P(i, pi/2)) +\
             P(i, (3*pi)/4)*log(P(i, (3*pi)/4)))


