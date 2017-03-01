#!/usr/bin/python -OO
# -*- encoding: iso-8859-1 -*-

if __name__=='__main__':

    from solver import *
    from rubik import *
    from time import time

    scrambling = 10
    rubik = RubikCube()
    scramble(rubik, scrambling) #, fixed=[3,10,2,5,5,5,4,7,4,8,1,11,9,9,4,15,6,17])
    print rubik
    resolve(rubik, error6, tmax = 1800, par=scrambling, max_level = scrambling + 2)
    
    