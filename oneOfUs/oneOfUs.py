import requests
import urllib
import random
import math


def start():

	while True:
		neighbors = getNeighbors()
		sol = solve(neighbors)
		sendSolution(sol)


def sendSolution(sol):
	dim = int(math.sqrt(len(sol)))
	strSol = ''
	for i in range(len(sol)):
		strSol += str( format( sol[i]%dim, '01X') ) + "," + str( format( sol[i]/dim, '01X') ) + "_" 
	
	strSol = strSol[:-1]
	print strSol
	#payload = {'name': 'SpaceMonkey', 'password': '******', 'path': strSol}
	#r = requests.post("http://www.hacker.org/oneofus/", params=payload)
	params = urllib.urlencode({'name': 'SpaceMonkey', 'password': '******', 'path': strSol})
	f = urllib.urlopen("http://www.hacker.org/oneofus/", params)
	print "Loesung gesendet! \n"
	

def getNeighbors():
	htmlCode = requests.get('http://www.hacker.org/oneofus/', params={'name': 'SpaceMonkey', 'password': 'schlurps123'}).content
	index = htmlCode.find('FlashVars') + 20
	dimx = ""
	dimy = ""
	board = []
	
	#get x-dimension
	while htmlCode[index] != '&':
		dimx += htmlCode[index]
		index += 1
		
	#get y-dimension	
	index += 3
	while htmlCode[index] != '&':
		dimy += htmlCode[index]
		index += 1
		
	#get the board	
	index += 7
	while htmlCode[index] != '"':
		board.append( htmlCode[index] + htmlCode[index+1] + htmlCode[index+2] + htmlCode[index+3] )
		index += 4

	(dimx, dimy) = (int(dimx),int(dimy))	
	neighbors = []
	
	for i in range(dimx):
		for j in range(dimy):
		
			neighbors.append([])
			currentElem = board[i*dimx+j]
			xaxis = range(dimx)
			yaxis = range(dimy)
			
			del xaxis[j]
			del yaxis[i]
			
			for k in xaxis:
				if (board[i*dimx + k][:2]) == currentElem[:2] or board[i*dimx + k][2:4] == currentElem[2:4]:
					neighbors[-1].append(i*dimx + k)
					
			for k in yaxis:
				if board[k*dimx + j][:2] == currentElem[:2] or board[k*dimx + j][2:4] == currentElem[2:4]:
					neighbors[-1].append(k*dimx + j)
	
	return neighbors

def solve(neighbors):
	
	length = len(neighbors)
	occupied = [0]*length
	directionFlag = 0
	foundFlag = 0

	current = random.randrange(length)
	occupied[current] = 1
	counter = 1
	
	currentPath = [current]
	
	while counter != length:
		
		foundFlag = 0
	
		#solve in random direction
		if (directionFlag == 0):
			direction = random.randrange(2)
		else:
			direction = direction ^ 1
			
		current = currentPath[ - direction ]
	
		#find a new neighbor and move on, if possible
		currentNeighbors = neighbors[ current ]
		
		numberOfNeighbors = len(currentNeighbors)
		randomList = random.sample( range(numberOfNeighbors), numberOfNeighbors )
		
		for i in randomList:
			if (occupied[currentNeighbors[i]] == 0):
				foundFlag = 1
				occupied[currentNeighbors[i]] = 1
				counter += 1
				if(direction == 0):
					currentPath.insert(0, currentNeighbors[i])
				else:
					currentPath.append(currentNeighbors[i])
				break
	
		#if a new neighbor wasn't found...
		if (foundFlag == 0):
			#1. Chose the other direction
			if (directionFlag == 0):
				directionFlag = 1
				continue
			#2. Or rebuild the path
			else:
				directionFlag = 0
				next = currentNeighbors[ random.randrange( numberOfNeighbors ) ]
				newIndex = currentPath.index(next)
				if (direction == 0):
					newFront = currentPath[:newIndex]
					newFront.reverse()
					currentPath = newFront + currentPath[newIndex:]
				else:
					newTail = currentPath[newIndex+1:]
					newTail.reverse()
					currentPath = currentPath[:newIndex+1] + newTail
	
	return currentPath
