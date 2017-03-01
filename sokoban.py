#!/usr/bin/env python -OO

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
        x, y = self._get_position()
        self._put_cell(x, y, TYPE_EMPTY)
        self.player_x = x
        self.player_y = y

    # Public methods
    
    def up(self):
        #x, y = self._get_position()
        x, y = self.player_x, self.player_y
        self._push(x, y - 1)

    def down(self):
        #x, y = self._get_position()
        x, y = self.player_x, self.player_y
        self._push(x, y + 1)

    def left(self):
        #x, y = self._get_position()
        x, y = self.player_x, self.player_y
        self._push(x - 1, y)

    def right(self):
        #x, y = self._get_position()
        x, y = self.player_x, self.player_y
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
        #x0, y0 = self._get_position()
        x0, y0 = self.player_x, self.player_y
        cell_type = self._get_cell(x, y) 
        if cell_type in (TYPE_EMPTY, TYPE_EMPTY_TARGET):
            self.player_x = x
            self.player_y = y        
        elif cell_type in (TYPE_BOX, TYPE_FILLED_TARGET):
            next_cell_type = self._get_cell(2 * x - x0, 2 * y - y0)
            if next_cell_type in (TYPE_EMPTY, TYPE_EMPTY_TARGET):
                #self._put_cell(x0, y0, TYPE_EMPTY)
                self._put_cell(x, y, TYPE_EMPTY if cell_type == TYPE_BOX else TYPE_EMPTY_TARGET)
                self._put_cell(2 * x - x0, 2 * y - y0, TYPE_BOX if next_cell_type == TYPE_EMPTY else TYPE_FILLED_TARGET)
                self.player_x = x
                self.player_y = y

    def _can_be_pushed(self, x, y):
        neighbours = (self.soko_map[y-1][x], self.soko_map[y][x+1], self.soko_map[y+1][x], self.soko_map[y][x-1])
        free = [i in (TYPE_BOX, TYPE_EMPTY, TYPE_EMPTY_TARGET) for i in neighbours]
        """0000  0
        0001  0
        0010  0
        0011  0
        0100  0
        0101  1
        0110  0
        0111  1
        1000  0
        1001  0
        1010  1
        1011  1
        1100  0
        1101  1
        1110  1
        1111  1
        1,1,1,1 1
        0,1,1,1 0"""
        
        return (free[0] and free[2]) or (free[1] and free[3])

    def __str__(self):
        #x, y = self._get_position()
        x, y = self.player_x, self.player_y
        _map = copy(self.soko_map)
        map_y = list(_map[y])
        map_y[x] = TYPE_PLAYER
        _map[y] = ''.join(map_y)
        return """\n""".join(_map)

def error_sokoban(obj):
    boxes_around = ''.join(obj.soko_map[obj.player_y-1:obj.player_y+1]).count(TYPE_BOX)
    return ''.join(obj.soko_map).count(TYPE_BOX) * (1 - boxes_around / 10.0) 

def error_sokoban2(obj):
    boxes = ''.join(obj.soko_map).count(TYPE_BOX)
    pushables = 0
    for y, line in enumerate(obj.soko_map):
        x_ant = 0
        for _ in range(line.count(TYPE_BOX)):
            x = line.index(TYPE_BOX, x_ant)
            x_ant = x + 1
            pushables += obj._can_be_pushed(x, y)
    return 40 * boxes - pushables 

if __name__ == "__main__":
    
    soko = Sokoban(SOKOBAN_MAP)
    
    # Play 20 random movements
    for i in range(20):
        direction = choice(['up', 'down', 'left', 'right'])
        print("Play ", direction)
        getattr(soko, direction)()
        print(soko)

