import copy
import mechanize
import cookielib

br = mechanize.Browser()

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
        for j in xrange( 0, getSIZE(gamedata)[0] ):
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
            print field[i][j],
        print ''


def recPathfinder(currentPath, field, length, solution):

    currentPos = currentPath[-1]
    
    i = 0
    lenOfField = len(field)
    while(True):
        x = currentPos[0]+i*currentPath[0][0]
        y = currentPos[1]+i*currentPath[0][1]
        if(x < lenOfField and y < lenOfField):
            if(field[x][y] == 1):
                return 0
            i += 1
        else: 
            break    
        
    
    if(length == 0):
        br.open('http://www.hacker.org/runaway/index.php?path=' + solution[::-1])
        print "\nLoesung gesendet! \n"
        return 1

    if(currentPos[0] >= 0 and currentPos[1] - 1 >= 0):
        
        currentPath.append( [currentPos[0], currentPos[1] - 1] )
        solution += 'R'
        result = recPathfinder(copy.deepcopy(currentPath), field, length - 1, solution)
        
        if(result == 1):
            return 1
        else:
            solution = solution[:-1]
    
      
    if(currentPos[0] - 1 >= 0 and currentPos[1] >= 0):
        
        currentPath[-1] = [currentPos[0] - 1, currentPos[1]]
        solution += 'D'
        result = recPathfinder(copy.deepcopy(currentPath), field, length - 1, solution)
        
        if(result == 1):
            return 1
        else:
            solution = solution[:-1]
        
    
    return 0
    
def getGameDataAsString(gamedataHTML):

    start = gamedataHTML.find('FVterrainString')
    gamedata = ''
    i = 0
    
    while(gamedataHTML[start+i] is not '"'):
        gamedata += gamedataHTML[start+i]
        i += 1
        
    gamedata += '&'    
    return gamedata


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
    
    for i in range(sizeX/3):
        for j in range(sizeX/3):
            sum3 += field[i][j]

    for i in range(sizeX/4):
        for j in range(sizeX/4):
            sum4 += field[i][j]
    
    for i in range(sizeX/6):
        for j in range(sizeX/6):
            sum6 += field[i][j]
            
    size3 = sizeX*sizeX/9
    size4 = sizeX*sizeX/16
    size6 = sizeX*sizeX/36

    if( ( sum3/float(size3) + sum4/float(size4) + sum6/float(size6) ) / 3 > limit ):
        return 1
    else:
        return 0

def main():

    # user data
    username = 'SpaceMonkey'   # your username/email
    password = '******'   # your password
    
    # set cookies
    cookies = cookielib.LWPCookieJar()
    br.set_cookiejar(cookies)
    
    br.open('http://www.hacker.org/forum/login.php')
    br.select_form(nr=0)
    
    br['username'] = username
    br['password'] = password
    br.submit()
    
    
    while(True):

        data = br.open('http://www.hacker.org/runaway/')
        gamedataHTML = ''
        
        while True:
            dataHTML = data.read()
            #print dataHTML
            if not dataHTML:         
                break
            gamedataHTML += dataHTML
        

        gamedata = getGameDataAsString(gamedataHTML)
        
        lvl = getLVL(gamedata)
        sizeX = getSIZE(gamedata)[0]
        sizeY = getSIZE(gamedata)[1]
        field = getFIELD(gamedata)
        insMin = getMINMAX(gamedata)[0]
        insMax = getMINMAX(gamedata)[1]
        
        print "Level: " + str(lvl)
        print "- Spielfeldgroesse: " + str(sizeX) + " * " + str(sizeY)
        print "- Minimale Schleifenlaenge: " + str(insMin)
        print "- Maximale Schleifenlaenge: " + str(insMax)
        solution = ''
        
        #feld wird ausgesucht
##        limit = 0.22
##        print "Suche nach geeignetem Feld ...",
##        while(True):
##            gamedataHTML = br.open('http://www.hacker.org/runaway/index.php?gotolevel=' + str(lvl) + '&go=Go+To+Level').read()
##            gamedata = getGameDataAsString(gamedataHTML)
##            sizeX = getSIZE(gamedata)[0]
##            field = getFIELD(gamedata)
##            if(checkField(field, sizeX, limit) == 1 or sizeX < 100):
##                break
##            limit -= 0.001
##            print ".",
        #ende der suche
        
        print ""
        
        print 'Starte Pfadberechnung...',        
        
        for currentLength in range(insMin, insMax + 1 ):
            
            lastPoints = generateLastPoints(field, currentLength)
            print ".",  
            
            for currentLastPoint in lastPoints: 

                result = recPathfinder([currentLastPoint], field, currentLength, solution)
                if(result == 1): 
                    break
                
            if(result == 1): 
                    break

        print ""


if __name__ == '__main__':
    main()
