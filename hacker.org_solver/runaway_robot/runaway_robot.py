import copy

def getLVL(gamedata):
    lvl = ''
    pos = gamedata.find('FVlevel') + 8
    while gamedata[pos] is not '&':
        lvl += gamedata[pos]
        pos += 1
    return int(lvl)
    
    
def getFIELD(gamedata):
    fieldUNICODE = ''
    pos = gamedata.find('FVterrainString') + 16
    while gamedata[pos] != '&':
        fieldUNICODE += gamedata[pos]
        pos += 1
        
    field = []
    for i in range( 0, getSIZE(gamedata)[1] ):
        field.append([])
        for j in range( 0, getSIZE(gamedata)[0] ):
            if( fieldUNICODE[ ( i * getSIZE(gamedata)[0] ) + j ] == '.' ):
                field[i].append( 0 )
            else:
                field[i].append( 1 )
            
    return field


def getSIZE(gamedata):
    x = ''
    pos = gamedata.find('FVboardX') + 9
    while gamedata[pos] != '&':
        x += gamedata[pos]
        pos += 1
    
    y = ''
    pos = gamedata.find('FVboardY') + 9
    while gamedata[pos] != '&':
        y += gamedata[pos]
        pos += 1

    return [int(x),int(y)]


def getMINMAX(gamedata):
    minX = ''
    pos = gamedata.find('FVinsMin') + 9
    while gamedata[pos] != '&':
        minX += gamedata[pos]
        pos += 1
     
    minY = ''
    pos = gamedata.find('FVinsMax') + 9
    while gamedata[pos] != '&':
        minY += gamedata[pos]
        pos += 1
 
    return [int(minX),int(minY)]


def printField(field):
    for i in range(len(field)):
        for j in range (len(field[i])):
            print(field[i][j]),
        print('')


def recPathfinder(currentPath, field, length, solution):
    currentPos = currentPath[-1]
    i = 0
    lenOfField = len(field)

    while(True):
        x = currentPos[0]+i*currentPath[0][0]
        y = currentPos[1]+i*currentPath[0][1]
        if(x < lenOfField and y < lenOfField):
            if(field[x][y] == 1):
                return False
            i += 1
        else: 
            break    
    
    if(length == 0):
        return solution[::-1]

    if(currentPos[0] >= 0 and currentPos[1] - 1 >= 0):
        currentPath.append( [currentPos[0], currentPos[1] - 1] )
        solution += 'R'
        result = recPathfinder(copy.deepcopy(currentPath), field, length - 1, solution)
        if(result != False):
            return result
        else:
            solution = solution[:-1]
    
      
    if(currentPos[0] - 1 >= 0 and currentPos[1] >= 0):
        currentPath[-1] = [currentPos[0] - 1, currentPos[1]]
        solution += 'D'
        result = recPathfinder(copy.deepcopy(currentPath), field, length - 1, solution)
        if(result != False):
            return result
        else:
            solution = solution[:-1]
    
    return False

    
def generateLastPoints(field, currentLength):
    lastPoints = []
    for i in range(currentLength+1):
        if( field[currentLength-i][i] == 0):
            lastPoints.append([currentLength-i, i])

    return lastPoints


def checkField(field, sizeX, limit):
    sum3 = 0
    sum4 = 0
    sum6 = 0
    
    for i in range(int(sizeX/3)):
        for j in range(int(sizeX/3)):
            sum3 += field[i][j]

    for i in range(int(sizeX/4)):
        for j in range(int(sizeX/4)):
            sum4 += field[i][j]
    
    for i in range(int(sizeX/6)):
        for j in range(int(sizeX/6)):
            sum6 += field[i][j]
            
    size3 = sizeX*sizeX/9
    size4 = sizeX*sizeX/16
    size6 = sizeX*sizeX/36

    if( ( sum3/float(size3) + sum4/float(size4) + sum6/float(size6) ) / 3 > limit ):
        return True
    else:
        return False

def solve(raw_board, info_flag=False, limit=0.25):
    gamedata = raw_board + '&'
    lvl = getLVL(gamedata)
    sizeX = getSIZE(gamedata)[0]
    sizeY = getSIZE(gamedata)[1]
    field = getFIELD(gamedata)
    insMin = getMINMAX(gamedata)[0]
    insMax = getMINMAX(gamedata)[1]
    solution = ''

    if info_flag:
        print("----------------------------------------------------------")
        print("Level: " + str(lvl))
        print("- Board size: " + str(sizeX) + " * " + str(sizeY))
        print("- Minimum loop length: " + str(insMin))
        print("- Maximum loop length: " + str(insMax))

    #board is chosen
    if info_flag:
        print("Searching for suitable board, this might take some time ...")
    if(checkField(field, sizeX, limit) == False and sizeX > 100):
        return (False, limit-0.001)

    if info_flag:
        print("\nFound suitable board!")
        print('Starting path calculations ...\nProgress: ', end="")        
     
    for currentLength in range(insMin, insMax + 1 ):
        lastPoints = generateLastPoints(field, currentLength)
        if info_flag:
            print(".", end="", flush=True)  
            
        for currentLastPoint in lastPoints: 
            result = recPathfinder([currentLastPoint], field, currentLength, solution)
            if(result != False): 
                break
                
        if(result != False): 
            break

    if info_flag:
        print("\n----------------------------------------------------------") 
    
    return (True, {'path': result})
