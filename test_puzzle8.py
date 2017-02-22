#!/usr/bin/pypy -OO
# -*- encoding: iso-8859-1 -*-

if __name__=='__main__':

    from solver import *
    from puzzlex import PuzzleX, scramble, errorPuzzle, PUZZLE8
    from time import time

    scrambling = 14
    puzzle = PuzzleX(PUZZLE8)
    scramble(puzzle, scrambling)
    print puzzle
    resolve(puzzle, errorPuzzle, tmax = 10, par=scrambling*2, max_level = scrambling)
    
    