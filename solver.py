#!/usr/bin/python -OO
# -*- encoding: iso-8859-1 -*-

from types import *
from copy import copy, deepcopy
from time import sleep,time
from thread import *
from Queue import Queue, Empty
#from Queue import PriorityQueue as PQueue

import sys

# Constantes

SOLVED=0
LIM_TIMEOUT=1
LIM_THREADS=2
LIM_MEMORY=3
NOT_SOLVED=4

# Variables globales

Result=0
SolHash=None
Timeout=0.0
Methods=None
NumMethods=0
Tolerance=0.0
MaxParallel=1000
MinLevel=0
MaxLevel=0
MaxLevelLimit=1000

# Objetos

Levels=None
Status=None
ErrFunc=None
Lock=None

"""	
El objeto es el problema, una instancia de una clase con algunos métodos
públicos sin parámetros, que servirán de acciones posibles para buscar una
solución.

La función de error recoge una instancia del problema, y devuelve un número
flotante, que significa la distancia hasta la solución. Puede implementar todas
las ecuaciones que quiera, pero basadas solamente, en la información de la
misma instancia del problema que coge como parámetro

Timeout, se usa para no aceptar soluciones que tarden más de X (en segundos)
tiempo en ejecutarse. Según la función de error, siempre se tenderá a ejecutar
primero el camino que llegue antes a la solución, así que con que pase el
tiempo indicado, se corta todo el problema, y se devuelve una solución parcial

La tolerancia, es una forma de indicar que no hace falta conseguir una solución
perfecta, sino un estado del problema, que esté más cerca de ella. Los valores
posibles van de 0 a 1, y toman, como 100%, a la distancia del estado inicial, a
una solución

El máximo de paralelismo sirve para limitar el máximo de niveles explorados
simultáneamente. El límite físico lo marca el sistema operativo, con 1024
threads al mismo tiempo. Cuanto más complicado sea un problema, menor deberá
ser el paralelismo.


"""

def solve (obj,errFunc,timeout=0.0,tolerance=0.0,maxParallel=1000, maxLevelLimit=1000, maxErrorAllowed=float("inf")):

	global Levels,Status,ErrFunc,Result,SolHash,Timeout,Methods,NumMethods,Tolerance,MaxParallel,Lock,MinLevel,MaxLevel,MaxLevelLimit, MaxErrorAllowed

	# Inicializa las variables globales
	Levels={}
	Status={}
	Result=NOT_SOLVED
	SolHash=None
	ErrFunc=errFunc
	Timeout=timeout
	MaxParallel=1000
	MinLevel=0
	MaxLevel=0
	MaxLevelLimit=max(MaxParallel, maxLevelLimit)
	MaxErrorAllowed = maxErrorAllowed
	
	# Incializa las locales
	objhash=getHash(obj)
	distance=ErrFunc(obj)

	# Recoge la lista de metodos
	rsc=obj.__class__.__dict__
	Methods=[]
	for i in rsc.keys():
		if (type(rsc[i])==FunctionType):
			if (not i[0]=='_'):
				Methods.append(i)
	NumMethods=len(Methods)
	
	# Calcula la tolerancia para la solución
	Tolerance=distance*tolerance

	# Inicializa el nivel máximo de paralelismo
	MaxParallel=maxParallel

	# Inicializa el bloqueo para el hash de Status
	Lock=allocate_lock()

	# Nivel actual
	level=0

	# Crea la cola e inserta el primer elemento del nivel 0
	Levels[level]=PQueue()
	Levels[level].put([objhash,0,-1,distance,None,obj])

	_solve(0)

	t0=time()
	printerr("solving...")
	while (Result==NOT_SOLVED):
		sleep(1)
		
		l=[]
		i=1
		while (i<len(Levels)):
			l.append(Levels[i].qsize())
			i=i+1
		printerr("{}\033[1A".format(l), )
		if (Timeout):
			tt=time()-t0
			if (tt>=Timeout):
				Result=LIM_TIMEOUT

	# Da una solución parcial si no hay total
	if (SolHash==None):
		if (len(Status.keys())):
			SolHash=objhash
		lev=0
		dis=0
		for i in Status.keys():
			if (Status[i][0]>lev):
				SolHash=i
				lev=Status[i][0]
				dis=Status[i][2]
			else:
				if (Status[i][0]==lev):
					if (dis>Status[i][2]):
						SolHash=i
						lev=Status[i][0]
						dis=Status[i][2]

#	printerr("Solution: %s" % (Status[SolHash]))
	printerr("\nLevels: %d/%d/%d" % (MinLevel,Status[SolHash][0],len(Levels)))
	return (Result,Status,SolHash,Methods)

def _solve (level):

	global Levels,Result,SolHash,Methods,NumMethods,ErrFunc,Tolerance,Lock,MinLevel,MaxLevel, MaxLevelLimit, MaxErrorAllowed

	while (Result==NOT_SOLVED):
		if ((level-MinLevel)<MaxParallel):

			# Recoge un nodo de la cola
			try:
				(objhash,order,method,distance,father,obj)=Levels[level].get_nowait()
				
				if distance > MaxErrorAllowed:
				    sleep(0.1)
				    continue
				
				# Guarda el nodo actual en el hash de estados # Status[objhash]=[nivel,metodo,distancia,padre]
				if insertState(objhash,level,method,distance,father):

					# Check if it's a solution
					if (distance<=Tolerance):
						SolHash=objhash
						Result=SOLVED
						printerr("%d: Found solucion. Size left: %d" % (level,Levels[level].qsize()))

					# Solo empieza con el siguiente nivel, si no esta solucionado y cuando no hemos llegado al MaxLevelLimit
					if Result==NOT_SOLVED and level <= MaxLevelLimit:

						# Si el error actual es mayor que el error de cabeza
						# del nivel anterior, hay una espera
						if level>0 and level>MinLevel:
							ant=Levels[level-1]
							if len(ant.queue) and distance>ant.queue[0][3]:
									sleep(0.1)
						
						# Inicializa el nivel+1, solo si no existe ya
						Lock.acquire()
						if (level+1 not in Levels.keys()):
							Levels[level+1]=PQueue()
							if (level+1>MaxLevel):
								MaxLevel=level+1
							start_new_thread(_solve,(level+1,))
						Lock.release()

						# Crea los estados para el proximo nivel
						i=0
						mnewdist=0
						while i < NumMethods:
							if method!=-1 and (i+9==method or i-9==method):
							    i+=1
							    continue
							newobj=deepcopy(obj)
							getattr(newobj,Methods[i])()
							newdist=ErrFunc(newobj)
							newhash=getHash(newobj)
							mnewdist=mnewdist+newdist
							Levels[level+1].put([newhash,-newdist,i,newdist,objhash,newobj])
							i=i+1

						# Parece ser que si la suma de distancias por cada método
						# en el nivel siguiente, es mayor que la distancia actual
						# multiplicada por el número de métodos, se queda en espera
						# el estado actual.
						"""
						if (mnewdist>distance*NumMethods):
							j=0
							while (level-MinLevel and j<2):
								espera=NumMethods*0.00001
								sleep(espera)
								j=j+1
						"""
																			
			except KeyError:
				#pass
				printerr("KeyErr: Sospechoso")
			
			except Empty:
				if (MinLevel==level and MaxLevel>level):
					if (Levels[MinLevel].qsize()==0):
						MinLevel=level+1
						break
					
				#printerr("%d: Esperando a que se llene la cola para seguir procesando" % (level))
				sleep(0.1)	# Espera a que se llene la cola
					
					
		else:
			#printerr("%d: Maximo paralelismo de colas alcanzado. Esperando..." % (level))
			sleep(1*level)
		
#	printerr("Nivel %d saliendo" % level)

# Herramientas

# Devuelve el identificador del objeto, que depende de su estado actual
def getHash (obj):

    rsc=vars(obj)
    for i in rsc.keys():
        if (i[0]=='_'):
            del rsc[i]
    result=str(rsc.values())
    return result	


# Inserta el estado, sólo si no existía, y devuelve el resultado (si es 1, puedo seguir creando nodos)
def insertState (objhash,level,method,distance,father):

	global Status,Lock

	result=1

	#Lock.acquire()

	if not objhash in Status.keys():
		Status[objhash]=[level,method,distance,father]
	else:
		if (level<Status[objhash][0]):
			#printerr("Atajo de %d pasos" % (Status[objhash][0]-level))
			Status[objhash]=[level,method,distance,father]
		result=0
		
	#Lock.release()

	return result

# Implementacion de la cola con prioridad, adaptada a solver
# El formato del item es: [hash,FatherDistance-distance,method,distance,fatherHash]

class PQueue (Queue):

	def _init (self,maxsize):
		self.maxsize=maxsize
		self.hsize=0
		self.queue=[]

	def _get(self):
		item = self.queue[0]
		del self.queue[0]
		return item

	def _put (self,item):
		l=len(self.queue)
		if l:
			if (l>self.hsize):
				self.hsize=l
			i=0
			thash=item[0]
			tdist=item[1]
			while tdist<=self.queue[i][1]:
				if thash==self.queue[i][0]:
					return
				i=i+1
				if i>=l:
					break
			self.queue.insert(i, item)
		else:
			self.queue.insert(0, item)


# Devuelve el camino hasta la solucion
def getSolution ():

	global SolHash,Status,Methods

	sol=[]
	i=SolHash
	while (not Status[i][3]==None):
		sol.insert(0,Methods[Status[i][1]])
		i=Status[i][3]

	return sol
	
def printerr (t):
	sys.stderr.write(str(t)+"\n")


def resolve (obj,err,tmax=60,tol=0,par=10, max_level=10, max_error=float("inf")):
	
    t0=time()
    (res,stat,sol,met)=solve(obj,err,tmax,tol,par,max_level, max_error)

    tt=time()-t0
    if (tt>=tmax and not tmax==0):
        cad="Timeout, partial solution (%d segs) \n" % (tmax)
    else:
        cad="Time: %d segs\n" % (tt)
	
    cad += "Nodes/sec {}\n".format(len(stat)/tt)
    print(cad)
    raw_input()
    sol=getSolution()
    for i in sol:
        sleep(0.5)
        getattr(obj,i)()
        print(obj)

    cad=cad+str(sol)
    print(cad)
    sleep(1)
