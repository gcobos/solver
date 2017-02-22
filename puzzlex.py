#!/usr/bin/pypy -OO
# -*- encoding: iso-8859-1 -*-

from solver import *
from string import upper, find
from time import sleep,time
from random import Random

import sys,os

# Problema ejemplo: Puzzle de bloques móviles

"""
	Los símbolos son:
	
	     Hueco vacío
	A..Z Piezas a ordenar
	
"""

PUZZLE8=["FHD",
		" GB",
		"CAE",
]

PUZZLE15=["HBAE",
		"GC K",
		"IFJD"
]

class PuzzleX:

	def __init__ (self,puzzle):
		self.puzzle=puzzle
			
	def __repr__ (self):
		cad=""
		for i in self.puzzle:
			cad=cad+i+"\n"
		return cad

	def up (self):
		(x,y)=self._getPos(' ')
		if (self._inRange(x,y+1)):
			self._swap(x,y,x,y+1)
	
	def down (self):
		(x,y)=self._getPos(' ')
		if (self._inRange(x,y-1)):
			self._swap(x,y,x,y-1)
		
	def right (self):
		(x,y)=self._getPos(' ')
		if (self._inRange(x-1,y)):
			self._swap(x,y,x-1,y)

	def left (self):
		(x,y)=self._getPos(' ')
		if (self._inRange(x+1,y)):
			self._swap(x,y,x+1,y)

	# Métodos privados
	
	# Devuelve la primera posición que contenga el carácter c
	def _getPos (self,c):
		y=0
		while (y<len(self.puzzle)):
			x=self.puzzle[y].find(c)
			if (x>-1):
				return (x,y)
			y=y+1
		return (-1,-1)						# Carácter no encontrado en el mapa

	# Devuelve el carácter en la posición indicada
	def _getAt (self,x,y):
		return self.puzzle[y][x]

	# Devuelve el carácter en la posición indicada
	def _inRange (self,x,y):
		if (y>=0 and y<len(self.puzzle)):
			if (x>=0 and x<len(self.puzzle[0])):
				return 1
		return 0

	# Pone un carácter en la posición indicada
	def _setAt (self,x,y,c):
		self.puzzle[y]=self.puzzle[y][0:x]+c+self.puzzle[y][x+1:]
		
	# Intercambia la posición de dos caracteres del puzzle
	def _swap (self,x,y,x2,y2):
		c=self._getAt(x,y)
		c2=self._getAt(x2,y2)
		self._setAt(x2,y2,c)
		self._setAt(x,y,c2)

# Función que devuelve la distancia entre el estado actual y la solución
def errorPuzzle (obj):
	err=0
	bloque='A'
	ancho=len(obj.puzzle[0])
	alto=len(obj.puzzle)
	pos=0

	while (bloque<='Z'):
		(x,y)=obj._getPos(bloque)
		x2=pos%ancho;
		y2=pos/ancho;
		if (x!=-1 and y2<alto):
			err=err+abs(x-x2)+abs(y-y2)
		bloque=chr(ord(bloque)+1)
		pos=pos+1
	return err

puzzle=PuzzleX(PUZZLE8)

def u():
	puzzle.up()
	return ''

def d():
	puzzle.down()
	return ''

def l():
	puzzle.left()
	return ''

def r():
	puzzle.right()
	return ''

def m(sec):
	for i in sec:
		if (i=='u'):
			puzzle.up()
		elif (i=='d'):
			puzzle.down()
		elif (i=='l'):
			puzzle.left()
		else:
		    puzzle.right()
	return ''

def scramble (puzzle, times, fixed = []):
	i=0
	r=Random()

	while (i<times):
		if fixed:
			v=int(fixed[i%len(fixed)])
		else:
			v=int((r.random()*18))
		
		if (v==0):
			puzzle.up()
		elif (v==1):
			puzzle.down()
		elif (v==2):
			puzzle.left()
		elif (v==3):
			puzzle.right()
		
		i=i+1

