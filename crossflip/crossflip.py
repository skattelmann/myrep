import ctypes
import numpy as np
import urllib
import requests
import time

def sendSolution(sol, n, level):
	strSol = ''
	for i in range(n):
		strSol += str(sol[i])
	
	params = urllib.urlencode({'name': 'SpaceMonkey', 'password': 'schniffi123', 'lvl': str(level), 'sol': strSol})
	f = urllib.urlopen("http://www.hacker.org/cross/", params)
	
	print "Loesung gesendet! \n"
	

def getGameData():

	payload = {'name': 'SpaceMonkey', 'password': 'schniffi123'}
	dataHTML = requests.get(url='http://www.hacker.org/cross/', params=payload).text

	start = dataHTML.find('boardinit')
	board = [[]]
	i = 0
	string = dataHTML[start+13+i]
	while(string != '"'):
		if string == ',':
			board.append([])
		else:
			board[-1].append(int(string))
		i += 1
		string = dataHTML[start+13+i]
		
	start = dataHTML.find('var level')
	level = ''
	i = 0
	string = dataHTML[start+12+i]
	while(string != ';'):
		level += string
		i += 1
		string = dataHTML[start+12+i]

	return ( np.array(board, dtype = 'i') , level)
      


def start():
  
	(gamedata, lvl) = getGameData()
	(n1,n2) = np.shape(gamedata) 
	
	Mrows = n1*n2
	Mcols = (n1*n2 + 1) / 64
	if (n1*n2 + 1) % 64 != 0:
		Mcols += 1

	M = np.zeros((Mrows,Mcols), dtype=np.uint64)
	x = np.zeros(n1*n2, dtype=np.int32)
	
	print "Level: " , lvl
	print "Groesse der Matrix: " , "{:,}".format( M.size )
	print "Normale Groesse: " , "{:,}".format( (n1*n2+1)*n1*n2 )
	
	tic = time.time()
	crossflip_helper.starter( ctypes.c_void_p(gamedata.ctypes.data) ,  ctypes.c_int(n1) ,  ctypes.c_int(n2) , ctypes.c_void_p(M.ctypes.data) , ctypes.c_void_p(x.ctypes.data) , ctypes.c_int(n1*n2) )
	toc = time.time() - tic

	print "Gauss-Elimination: " , toc , "s"
	
	sendSolution(x, n1*n2, lvl)
	
	
	
#################
crossflip_helper = ctypes.CDLL('/home/sascha/crossflip_1.1/crossflip_helper.so')
while 1:  
	start()