#!/usr/bin/pypy -OO
# -*- encoding: iso-8859-1 -*-

if __name__=='__main__':

    from solver import *
    from sokoban import *
    from time import time

    soko = Sokoban(SOKOBAN_MAP)
    print soko
    print resolve(soko, error_sokoban, tmax = 1800, par=30, max_level = 100)

