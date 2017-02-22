#!/usr/bin/pypy -OO
# -*- encoding: iso-8859-1 -*-

if __name__=='__main__':

    from solver import *
    from sokoban import *
    from time import time


    sokomap = """#############
#   #X     X#
#        O O#
#  #### ### #
# O #       #
#  ##   ##  #
#@  #   X   #
#############"""

    soko = Sokoban(sokomap)
    print soko
    resolve(soko, error_sokoban, tmax = 1800, par=40, max_level = 30)

