import ctypes
import numpy as np
import os
import time

curr_folder = os.getcwd()
crossflip_helper = ctypes.CDLL(curr_folder + '/crossflip/crossflip_helper.so')

def getGameData(raw_board):
	board = [[]]
	for i in range(len(raw_board)):
		if raw_board[i] == ',':
			board.append([])
		else:
			board[-1].append(int(raw_board[i]))
		
	return np.array(board, dtype = 'i')


def solve(raw_board, info_flag=False):
	gamedata = getGameData(raw_board)
	(n1,n2) = np.shape(gamedata) 
	
	Mrows = n1*n2
	Mcols = (n1*n2 + 1) / 64
	if (n1*n2 + 1) % 64 != 0:
		Mcols += 1

	M = np.zeros((Mrows,Mcols), dtype=np.uint64)
	x = np.zeros(n1*n2, dtype=np.int32)
	
	if info_flag:
		print("----------------------------------------------------------")
		print("Raw size of the matrix: " , "{:,}".format( M.size ))
		print("Normalized size: " , "{:,}".format( (n1*n2+1)*n1*n2 ))
	
	tic = time.time()
	crossflip_helper.starter( ctypes.c_void_p(gamedata.ctypes.data) ,  ctypes.c_int(n1) ,  ctypes.c_int(n2) , ctypes.c_void_p(M.ctypes.data) , ctypes.c_void_p(x.ctypes.data) , ctypes.c_int(n1*n2) )
	toc = time.time() - tic

	if info_flag:
		print("Gaussian Elimination: " , toc , "s")
		print("----------------------------------------------------------")
	
	strSol = ''
	for i in range(n1*n2):
		strSol += str(x[i])

	sol_params = {'sol': strSol}
	return (True, sol_params)	
	
	

