import random
import math
import numpy as np
import time

def recSearch(board, ii, jj, dirs):
    # bottom
    i = ii+1
    j = jj
    pos = board[i,j]
    if pos == 0:
        while pos == 0:
            board[i, j] = 1
            i += 1
            pos = board[i,j]
        i -= 1
        board[i,j] = 2
        dirs.append('d')
        result = recSearch(board, i, j, dirs)
        if result != False:
            return result
        else:
            dirs.pop()
            board[i,j] = 0
            pos = board[i,j]
            while pos != 2:
                board[i,j] = 0
                i -= 1
                pos = board[i,j]

    # top
    i = ii-1
    j = jj
    pos = board[i,j]
    if pos == 0:
        while pos == 0:
            board[i, j] = 1
            i -= 1
            pos = board[i,j]
        i += 1
        board[i,j] = 2
        dirs.append('u')
        result = recSearch(board, i, j, dirs)
        if result != False:
            return result
        else:
            dirs.pop()
            board[i,j] = 0
            pos = board[i,j]
            while pos != 2:
                board[i,j] = 0
                i += 1
                pos = board[i,j]

    # right
    i = ii
    j = jj+1
    pos = board[i,j]
    if pos == 0:
        while pos == 0:
            board[i, j] = 1
            j += 1
            pos = board[i,j]
        j -= 1
        board[i,j] = 2
        dirs.append('r')
        result = recSearch(board, i, j, dirs)
        if result != False:
            return result
        else:
            dirs.pop()
            board[i,j] = 0
            pos = board[i,j]
            while pos != 2:
                board[i,j] = 0
                j -= 1
                pos = board[i,j]

    # left
    i = ii
    j = jj-1
    pos = board[i,j]
    if pos == 0:
        while pos == 0:
            board[i, j] = 1
            j -= 1
            pos = board[i,j]
        j += 1
        board[i,j] = 2
        dirs.append('l')
        result = recSearch(board, i, j, dirs)
        if result != False:
            return result
        else:
            dirs.pop()
            board[i,j] = 0
            pos = board[i,j]
            while pos != 2:
                board[i,j] = 0
                j += 1
                pos = board[i,j]

    #print '.' ,
            
    if np.all(board!=0):
        return dirs
    else:
        return False


def getBoard(raw_board):
    htmlCode = raw_board
    index = 2
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
    while index < len(htmlCode):
        if htmlCode[index] == 'X':
            board.append( 1 )
        else:
            board.append( 0 )
        index += 1

    (dimx, dimy) = (int(dimx),int(dimy))    
    splitted_board = [ [1] + board[i:i+dimx] + [1] for i in range(0, dimx*dimy, dimx)]
    splitted_board.append((dimx+2)*[1])
    splitted_board.insert(0, (dimx+2)*[1])

    return np.array(splitted_board)


def solve(raw_board, info_flag=False):
    board = getBoard(raw_board)
    (dimx, dimy) = board.shape
    for i in range(1,dimx-1):
        for j in range(1,dimy-1):
            if board[i,j] == 0:
                board[i,j] = 2
                new_dirs = recSearch(board, i, j, [])
                if new_dirs != False:
                    sol_string = "".join(new_dirs).upper()
                    sol_params = {'x': str(j-1), 'y': str(i-1), 'path': sol_string}
                    return (True, sol_params)
                else:
                    board[i,j] = 0

                
