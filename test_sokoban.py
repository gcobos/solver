#!/usr/bin/env python -OO
# -*- encoding: iso-8859-1 -*-

if __name__=='__main__':

    from solver import *
    from sokoban import *
    from time import time

    sokomap1 = """#############
#   #X     X#
#        O O#
#  #### ### #
# O # X     #
#  ## O ##  #
#@  #   X   #
#############"""


    sokomap2 = """
##############
#XX  #     ###
#XX  # O  O  #
#XX  #O####  #
#XX    @ ##  #
#XX  # #  O ##
###### ##O O #
  # O  O O O #
  #    #     #
  ############"""


    sokomap3 = """
##############
#X   #     ###
#    #       #
#    # ####  #
#X     @ ##  #
#X   # #  O ##
###### ##O O #
  #          #
  #    #     #
  ############"""

    soko = Sokoban(sokomap1)
    print soko
    resolve(soko, error_sokoban, tmax = 0, par=100, max_level = 100, max_error=1000)

