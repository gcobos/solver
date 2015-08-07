#!/usr/bin/pypy -OO
# -*- encoding: iso-8859-1 -*-

from solver import solve,getSolution
from string import upper,find
from time import sleep,time
from random import Random
import sys,os

# Problema ejemplo: Cubo de rubik

RUBIK=[
	[0,0,0,0,0,0,0,0,0],	#   0
	[1,1,1,1,1,1,1,1,1],	#   1
	[2,2,2,2,2,2,2,2,2],	#  425
	[3,3,3,3,3,3,3,3,3],	#   3
	[4,4,4,4,4,4,4,4,4],
	[5,5,5,5,5,5,5,5,5],
]

ColorTable=(1,2,3,4,5,6)

class RubikCube:

	def __init__ (self, rubik = RUBIK):
		self.p=rubik
			
	def __repr__ (self):
		global ColorTable
	
		cad=""
		for i in range(0,3):
			cad=cad+"  "*3
			cad=cad+"\033[%dm  "%(100+ColorTable[self.p[0][i*3]])
			cad=cad+"\033[%dm  "%(100+ColorTable[self.p[0][i*3+1]])
			cad=cad+"\033[%dm  "%(100+ColorTable[self.p[0][i*3+2]])
			cad=cad+"\033[0m\n"

		for i in range(0,3):
			cad=cad+'  '*3
			cad=cad+"\033[%dm  "%(100+ColorTable[self.p[1][i*3]])
			cad=cad+"\033[%dm  "%(100+ColorTable[self.p[1][i*3+1]])
			cad=cad+"\033[%dm  "%(100+ColorTable[self.p[1][i*3+2]])
			cad=cad+"\033[0m\n"
	
		for i in range(0,3):
			cad=cad+"\033[%dm  "%(100+ColorTable[self.p[4][i*3]])
			cad=cad+"\033[%dm  "%(100+ColorTable[self.p[4][i*3+1]])
			cad=cad+"\033[%dm  "%(100+ColorTable[self.p[4][i*3+2]])
			cad=cad+"\033[%dm  "%(100+ColorTable[self.p[2][i*3]])
			cad=cad+"\033[%dm  "%(100+ColorTable[self.p[2][i*3+1]])
			cad=cad+"\033[%dm  "%(100+ColorTable[self.p[2][i*3+2]])
			cad=cad+"\033[%dm  "%(100+ColorTable[self.p[5][i*3]])
			cad=cad+"\033[%dm  "%(100+ColorTable[self.p[5][i*3+1]])
			cad=cad+"\033[%dm  "%(100+ColorTable[self.p[5][i*3+2]])
			cad=cad+"\033[0m\n"

		for i in range(0,3):
			cad=cad+'  '*3
			cad=cad+"\033[%dm  "%(100+ColorTable[self.p[3][i*3]])
			cad=cad+"\033[%dm  "%(100+ColorTable[self.p[3][i*3+1]])
			cad=cad+"\033[%dm  "%(100+ColorTable[self.p[3][i*3+2]])
			cad=cad+"\033[0m\n"			
		return cad

	def rotx1 (self):
		tmp=self._getLine(0,0,0)
		tmp.reverse()
		self._setLine(0,0,0,self._getLine(1,0,0))
		self._setLine(1,0,0,self._getLine(2,0,0))
		self._setLine(2,0,0,self._getLine(3,0,0))
		self._setLine(3,0,0,tmp)

		self._rotate(4,1)

	def rotx1n (self):
		self.rotx1()
		self.rotx1()
		self.rotx1()
	
	def rotx2 (self):
		tmp=self._getLine(0,0,1)
		tmp.reverse()
		self._setLine(0,0,1,self._getLine(1,0,1))
		self._setLine(1,0,1,self._getLine(2,0,1))
		self._setLine(2,0,1,self._getLine(3,0,1))
		self._setLine(3,0,1,tmp)

	def rotx2n (self):
		self.rotx2()
		self.rotx2()
		self.rotx2()

	def rotx3 (self):
		tmp=self._getLine(0,0,2)
		tmp.reverse()
		self._setLine(0,0,2,self._getLine(1,0,2))
		self._setLine(1,0,2,self._getLine(2,0,2))
		self._setLine(2,0,2,self._getLine(3,0,2))
		self._setLine(3,0,2,tmp)

		self._rotate(5,0)

	def rotx3n (self):
		self.rotx3()
		self.rotx3()
		self.rotx3()

	def roty1 (self):
		tmp=self._getLine(0,1,0)
		tmp.reverse()
		tmp1=self._getLine(5,1,2)
		tmp1.reverse()
		self._setLine(0,1,0,tmp1)
		self._setLine(5,1,2,self._getLine(2,1,2))
		self._setLine(2,1,2,self._getLine(4,1,2))
		self._setLine(4,1,2,tmp)
		
		self._rotate(3,0)

	def roty1n (self):
		self.roty1()
		self.roty1()
		self.roty1()

	def roty2 (self):
		tmp=self._getLine(0,1,1)
		tmp.reverse()
		tmp1=self._getLine(5,1,1)
		tmp1.reverse()
		self._setLine(0,1,1,tmp1)
		self._setLine(5,1,1,self._getLine(2,1,1))
		self._setLine(2,1,1,self._getLine(4,1,1))
		self._setLine(4,1,1,tmp)

	def roty2n (self):
		self.roty2()
		self.roty2()
		self.roty2()

	def roty3 (self):
		tmp=self._getLine(0,1,2)
		tmp.reverse()
		tmp1=self._getLine(5,1,0)
		tmp1.reverse()
		self._setLine(0,1,2,tmp1)
		self._setLine(5,1,0,self._getLine(2,1,0))
		self._setLine(2,1,0,self._getLine(4,1,0))
		self._setLine(4,1,0,tmp)
		
		self._rotate(1,0)

	def roty3n (self):
		self.roty3()
		self.roty3()
		self.roty3()

	def rotz1 (self):
		tmp=self._getLine(1,1,0)
		tmp.reverse()
		self._setLine(1,1,0,self._getLine(5,0,2))
		tmp1=self._getLine(3,1,2)
		tmp1.reverse()
		self._setLine(5,0,2,tmp1)
		self._setLine(3,1,2,self._getLine(4,0,0))
		self._setLine(4,0,0,tmp)

		self._rotate(0,0)

	def rotz1n (self):
		self.rotz1()
		self.rotz1()
		self.rotz1()
		
	def rotz2 (self):
		tmp=self._getLine(1,1,1)
		tmp.reverse()
		self._setLine(1,1,1,self._getLine(5,0,1))
		tmp1=self._getLine(3,1,1)
		tmp1.reverse()
		self._setLine(5,0,1,tmp1)
		self._setLine(3,1,1,self._getLine(4,0,1))
		self._setLine(4,0,1,tmp)

	def rotz2n (self):
		self.rotz2()
		self.rotz2()
		self.rotz2()

	def rotz3 (self):
		tmp=self._getLine(1,1,2)
		tmp.reverse()
		self._setLine(1,1,2,self._getLine(5,0,0))
		tmp1=self._getLine(3,1,0)
		tmp1.reverse()
		self._setLine(5,0,0,tmp1)
		self._setLine(3,1,0,self._getLine(4,0,2))
		self._setLine(4,0,2,tmp)

		self._rotate(2,0)

	def rotz3n (self):
		self.rotz3()
		self.rotz3()
		self.rotz3()

	# Métodos privados

	# Coge tres cuadros de una cara, sobre el eje indicado y el número de fila
	def _getLine (self,cara,eje,fila):
		if (eje==0):
			return [self.p[cara][0+fila],self.p[cara][3+fila],self.p[cara][6+fila]]
		else:
			return [self.p[cara][0+(fila*3)],self.p[cara][1+(fila*3)],self.p[cara][2+(fila*3)]]

	# Pone tres cuadros de una cara, sobre el eje indicado y el número de fila
	def _setLine (self,cara,eje,fila,linea):
		if (eje==0):
			self.p[cara][0+fila]=linea[0]
			self.p[cara][3+fila]=linea[1]
			self.p[cara][6+fila]=linea[2]
		else:
			self.p[cara][0+(fila*3)]=linea[0]
			self.p[cara][1+(fila*3)]=linea[1]
			self.p[cara][2+(fila*3)]=linea[2]

	def _rotate (self,cara,sentido):
		tmp1=self._getLine(cara,0,0)
		tmp2=self._getLine(cara,0,1)
		tmp3=self._getLine(cara,0,2)
		if (sentido==0):
			tmp1.reverse()
			tmp2.reverse()
			tmp3.reverse()
			self._setLine(cara,1,0,tmp1)
			self._setLine(cara,1,1,tmp2)
			self._setLine(cara,1,2,tmp3)
		else:
			self._setLine(cara,1,2,tmp1)
			self._setLine(cara,1,1,tmp2)
			self._setLine(cara,1,0,tmp3)
		
# Función que devuelve la distancia entre el estado actual y la solución

def error1 (obj):
	err=0
	for i in obj.p:
		prb=[]
		for j in (0,2,4,6,8):
			k=i[j]
			if (not k in prb):
				prb.append(k)
		err=err+(2*len(prb))-1
		prb=[]
		for j in (1,3,5,7):
			k=i[j]
			if (not k in prb):
				prb.append(k)
		err=err+(len(prb))-1
	return err

tablasol=(
    (0,1,2,3,4,5),
    (0,5,2,4,1,3),
    (0,3,2,1,5,4),
    (0,4,2,5,3,1),
    (1,2,3,0,4,5),
    (1,5,3,4,2,0),
    (1,0,3,2,5,4),
    (1,4,3,5,0,2),
    (2,3,0,1,4,5),
    (2,5,0,4,3,1),
    (2,1,0,3,5,4),
    (3,0,1,2,4,5),
    (3,5,1,4,0,2),
    (3,2,1,0,5,4),
    (3,4,1,5,2,0),
    (4,3,5,1,0,2),
    (4,2,5,0,3,1),
    (4,1,5,3,2,0),
    (4,0,5,2,1,3),
    (4,0,5,2,1,3),
    (5,3,4,1,2,0),
    (5,0,4,2,3,1),
    (5,1,4,3,0,2),
    (5,2,4,0,1,3),
)

def error2 (obj):
	global tablasol
	minerr=-1
	err=0
	for i in tablasol:
		err=0
		for j in i:
			err=err+(9-obj.p[j].count(j))
		if (minerr==-1 or err<minerr):
			minerr=err
	return minerr

def error3 (obj):
	err=0
	for i in obj.p:
		prb=[]
		for j in i:
			if (not j in prb):
				prb.append(j)
		err=err+len(prb)-1
	return err

def error4 (obj):
	global tablasol
	minerr=-1
	err=0
	for i in tablasol:
		err=0
		for j in i:
			err=err+(2*(9-obj.p[j].count(j)))
		if (minerr==-1 or err<minerr):
			minerr=err
	for i in obj.p:
		prb=[]
		for j in (0,2,6,8):
			k=i[j]
			if (not k in prb):
				prb.append(k)
		minerr=minerr+len(prb)-1
		prb=[]
		for j in i:	
			if (not j in prb):
				prb.append(j)
		minerr=minerr+len(prb)-1
	return minerr

def error5 (obj):
	global tablasol
	minerr=-1
	err=0
	for i in tablasol:
		err=0
		for j in i:
			err=err+((9-obj.p[j].count(j)))
		if (minerr==-1 or err<minerr):
			minerr=err
	for i in obj.p:
		prb=[]
		for j in (0,2,6,8):
			k=i[j]
			if (not k in prb):
				prb.append(k)
		minerr=minerr+len(prb)-1
		prb=[]
		for j in i:	
			if (not j in prb):
				prb.append(j)
		minerr=minerr+len(prb)-1
	return minerr

def scramble (rubik,times, fixed = []):
	i=0
	r=Random()

	while (i<times):
		if fixed:
			v=int(fixed[i%len(fixed)])
		else:
			v=int((r.random()*18))
		
		if (v==0):
			rubik.rotx1()
		elif (v==1):
			rubik.rotx2()
		elif (v==2):
			rubik.rotx3()
		elif (v==3):
			rubik.roty1()
		elif (v==4):
			rubik.roty2()
		elif (v==5):
			rubik.roty3()
		elif (v==6):
			rubik.rotz1()
		elif (v==7):
			rubik.rotz2()
		elif (v==8):
			rubik.rotz3()
		
		if (v==9):
			rubik.rotx1n()
		elif (v==10):
			rubik.rotx2n()
		elif (v==11):
			rubik.rotx3n()
		elif (v==12):
			rubik.roty1n()
		elif (v==13):
			rubik.roty2n()
		elif (v==14):
			rubik.roty3n()
		elif (v==15):
			rubik.rotz1n()
		elif (v==16):
			rubik.rotz2n()
		elif (v==17):
			rubik.rotz3n()
		
		i=i+1

