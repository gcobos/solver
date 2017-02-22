#!/usr/bin/python

from copy import copy
from random import choice

"""
    Simple implementation of Sokoban game to test the solver

    Symbols used in the maps are:

    # Wall
    O Box
    X Target for the box
    @ Player
"""

TYPE_EMPTY = " "
TYPE_WALL = "#"
TYPE_BOX = "O"
TYPE_EMPTY_TARGET = "X"
TYPE_FILLED_TARGET = "Y"
TYPE_PLAYER = "@"

SOKOBAN_MAP = """#############
#   #X     X#
#        O O#
#  #### ### #
# O #       #
#  ##   ##  #
#@  #   X   #
#############"""

class Sokoban(object):

    def __init__(self, _map = SOKOBAN_MAP):
        
        self.soko_map = copy(_map.splitlines())

    # Public methods
    
    def up(self):
        x, y = self._get_position()
        self._push(x, y - 1)

    def down(self):
        x, y = self._get_position()
        self._push(x, y + 1)

    def left(self):
        x, y = self._get_position()
        self._push(x - 1, y)

    def right(self):
        x, y = self._get_position()
        self._push(x + 1, y)

    # Internal methods

    def _get_position(self):
        for y, line in enumerate(self.soko_map):
            if TYPE_PLAYER in line:
                x = line.index(TYPE_PLAYER)
                break
        return x, y
    
    def _get_cell(self, x, y):
        return self.soko_map[y][x]

    def _put_cell(self, x, y, c):
        map_y = list(self.soko_map[y])
        map_y[x] = c
        self.soko_map[y] = ''.join(map_y)

    def _push(self, x, y):
        x0, y0 = self._get_position()
        cell_type = self._get_cell(x, y) 
        if cell_type == TYPE_EMPTY:
            self._put_cell(x0, y0, TYPE_EMPTY)
            self._put_cell(x, y, TYPE_PLAYER)
        elif cell_type == TYPE_BOX:
            next_cell_type = self._get_cell(2 * x - x0, 2 * y - y0)
            if next_cell_type in (TYPE_EMPTY, TYPE_EMPTY_TARGET):
                self._put_cell(x0, y0, TYPE_EMPTY)
                self._put_cell(x, y, TYPE_PLAYER)
                self._put_cell(2 * x - x0, 2 * y - y0, TYPE_BOX if next_cell_type == TYPE_EMPTY else TYPE_FILLED_TARGET)

    def __str__(self):
        return """\n""".join(self.soko_map)


def error_sokoban(obj):
    return str(obj).count(TYPE_EMPTY_TARGET)

if __name__ == "__main__":
    
    soko = Sokoban(SOKOBAN_MAP)
    
    # Play 20 random movements
    for i in range(20):
        direction = choice(['up', 'down', 'left', 'right'])
        print("Play ", direction)
        getattr(soko, direction)()
        print(soko)

