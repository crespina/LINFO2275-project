import numpy as np
import random
import copy

nSquares = 15

"""
layout : 
___________________________________________________________________
|  0  |  1  |  2  |  3  |  4  |  5  |  6  |  7  |  8  |  9  |  14  |
|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|______|
              \                                                / 
               \                                              /   
           _____\____________________________________________/____
          |    10      |      11      |      12      |     13     |
          |____________|______________|______________|____________|                    


"""

def proba_security_dice():
    
    proba = np.zeros((nSquares,nSquares))
    proba_prison = np.zeros((nSquares,nSquares))
    
    for i in range(nSquares-1):
        
        #1 chance out of 2 to stay at the same place
        proba[i][i] = 0.5
        
        #1 chance out of 2 to go 1 further
        if i == 2 :
            proba[i][i+1] = 0.25 #slow lane
            proba[i][i+8] = 0.25 #fast lane
            
        elif i == 9 :
            proba[i][i+5] = 0.5
            
        else :
            proba[i][i+1] = 0.5
    
    proba[nSquares-1][nSquares-1] = 1 #the end
    return proba, proba_prison

def proba_normal_dice(layout, circle):
    
    proba = np.zeros((nSquares,nSquares))
    proba_prison = np.zeros((nSquares,nSquares))
    for i in range(nSquares-1):
        
        #1 chance out of 3 to stay at the same place
        proba[i][i] = 1/3
        
        #1 chance out of 3 to go 1 further
        #1 chance out of 3 to go 2 further
        
        if i == 2 :
            proba[i][i+1] = 1/6 #slow lane
            proba[i][i+2] = 1/6 #slow lane
            proba[i][i+8] = 1/6 #fast lane
            proba[i][i+9] = 1/6 #fast lane
        
        elif i == 8 :
            proba[i][i+1] = 1/3
            proba[i][i+6] = 1/3
            
        elif i == 9 :
            if circle :
                proba[i][i+5] = 1/3
                proba[i][0] = 1/3
            else :
                proba[i][i+5] = 2/3
                
        elif i == 13 :
            if circle :
                proba[i][i+1] = 1/3
                proba[i][0] = 1/3
            else :
                proba[i][i+1] = 2/3
        
        else :
            proba[i][i+1] = 1/3
            proba[i][i+2] = 1/3
            
        #traps
            
    for i in range (nSquares-1):
        for j in range(nSquares-1) :
                
            match layout[j] :
                    
                case 1 : #restart
                    if j != 0 :
                        proba[i][0] += proba[i][j]/2
                        proba[i][j]/=2
                            
                case 2 : #penalty
                    proba[i][j-3 if j-3>=0 else 0] += proba[i][j]/2
                    proba[i][j]/=2
                    
                case 3 : #prison
                    proba_prison[i][j] = proba[i][j]/2
                    
                case 4 : #mystery
                        
                    proba[i][j]/=2 #don't activate the trap
                        
                    if j != 0 :
                        proba[i][0] += proba[i][j]/6 #trap restart
                            
                    proba[i][j-3 if j-3>=0 else 0] += proba[i][j]/6 #trap minus 3
                        
                    proba_prison[i][j] = proba[i][j]/6 #trap prison

    proba[nSquares-1][nSquares-1] = 1

    return proba, proba_prison

def proba_risky_dice(layout, circle):
    
    proba = np.zeros((nSquares,nSquares))
    proba_prison = np.zeros((nSquares,nSquares))
    for i in range(nSquares-1):
        
        #1 chance out of 4 to stay at the same place
        proba[i][i] = 1/4
        
        #1 chance out of 4 to go 1 further
        #1 chance out of 4 to go 2 further
        #1 chance out of 4 to go 3 further
        
        if i == 2 :
            proba[i][i+1] = 1/8 #slow lane
            proba[i][i+2] = 1/8 #slow lane
            proba[i][i+3] = 1/8 #slow lane
            
            proba[i][i+8] = 1/8 #fast lane
            proba[i][i+9] = 1/8 #fast lane
            proba[i][i+10] = 1/8 #fast lane
        
        elif i == 7 :
            proba[i][i+1] = 1/4
            proba[i][i+2] = 1/4
            proba[i][i+7] = 1/4
            
        elif i == 8 :
            if circle :
                proba[i][i+1] = 1/4
                proba[i][i+6] = 1/4
                proba[i][0] = 1/4
            else :
                proba[i][i+1] = 1/4
                proba[i][i+6] = 1/2
        
        elif i == 9 :
            if circle :
                proba[i][i+5] = 1/4
                proba[i][0] = 1/4
                proba[i][1] = 1/4
            else :
                proba[i][i+5] = 3/4
        
                
        elif i == 12 :
            if circle :
                proba[i][i+1] = 1/4
                proba[i][(i+2)] = 1/4
                proba[i][0] = 1/4
            else :
                proba[i][i+1] = 1/4
                proba[i][i+2] = 1/2

        elif i == 13 :
            if circle :
                proba[i][i+1] = 1/4
                proba[i][0] = 1/4
                proba[i][1] = 1/4
            else :
                proba[i][nSquares-1] = 3/4
        
        else :
            proba[i][i+1] = 1/4
            proba[i][i+2] = 1/4
            proba[i][i+3] = 1/4
         
    #traps
            
    for i in range (nSquares-1):
        for j in range(nSquares-1) :
                
            match layout[j] :
                    
                case 1 : #restart
                    if j != 0 :
                        proba[i][0] += proba[i][j]
                        proba[i][j] = 0
                            
                case 2 : #penalty
                    proba[i][j-3 if j-3>=0 else 0] += proba[i][j]
                    proba[i][j] = 0
                    
                case 3 : #prison
                    proba_prison[i][j] = proba[i][j]
                    
                case 4 : #mystery               
                       
                    if j != 0 :
                        proba[i][0] += proba[i][j]/3 #trap restart
                            
                    proba[i][j-3 if j-3>=0 else 0] += proba[i][j]/3 #trap minus 3

                    proba_prison[i][j] = proba[i][j]/3 #trap prison
                    proba[i][j] /= 3

    proba[nSquares-1][nSquares-1] = 1

    return proba, proba_prison                        
                
    

def markovDecision(layout,circle):
    """
        The function markovDecision takes a layout of the Snakes & Ladders game and returns the optimal strategy in terms of dice choice

        Args :

            layout (numpy.ndarray): represents the layout of the game, containing 15 values representing the 15 squares of the Snakes and Ladders game:
                                    layout[i] = 0 if it is an ordinary square
                                              = 1 if it is a “restart” trap (go back to square 1)
                                              = 2 if it is a “penalty” trap (go back 3 steps)
                                              = 3 if it is a “prison” trap (skip next turn)
                                              = 4 if it is a “mystery” trap (random effect among the three previous)

            circle (bool): indicates if the player must
                            - land exactly on the final square (15) to win (circle = True) or
                            - still wins by overstepping the final square (circle = False)

        Returns :

            Expec (numpy.ndarray): represents the expected cost (= number of turns) associated to the 14 squares of the game, excluding the goal square.
                                   The vector starts at index 0 (corresponding to square 1 on the example) and ends at index 13 (square 14).

            Dice (numpy.ndarray): contains the choice of the dice to use for each of the 14 squares of the game 
                                  (1 for “security” dice, 2 for “normal” dice and 3 for “risky”),
                                  excluding the goal square. Again, the vector starts at index 0 (square 1) and ends at index 13 (square 14).

    """
    proba_security, prison_security = proba_security_dice()
    proba_normal, prison_normal = proba_normal_dice(layout,circle)
    proba_risky, prison_risky = proba_risky_dice(layout,circle)

    value = np.zeros(nSquares)
    newValue = np.arange(nSquares-1,-1,-1)
    index=0
    while (sum(abs(newValue-value)) > 1e-9):
        index+=1
        print(index)
        value = copy.deepcopy(newValue)
        for i in range (nSquares-1):
            newValue[i] = 1 + min(np.dot(proba_security[i],value) + np.dot(prison_security[i],value), np.dot(proba_normal[i],value) + np.dot(prison_normal[i],value), np.dot(proba_risky[i],value) + np.dot(prison_risky[i],value))
        newValue[nSquares-1] = min(np.dot(proba_security[nSquares-1],value), np.dot(proba_normal[nSquares-1],value), np.dot(proba_risky[nSquares-1],value))

    dice = np.zeros(15, dtype=float)
    for i in range (nSquares):
        dice[i] = np.argmin([np.dot(proba_security[i],value) + np.dot(prison_security[i],value), np.dot(proba_normal[i],value) + np.dot(prison_normal[i],value), np.dot(proba_risky[i],value) + np.dot(prison_risky[i],value)])

    return newValue, dice


    
def playOneTurn(diceChoice, curPos, layout, circle, prison):
    """
    The function playOneTurn simulates one turn of the game, given the choice of dice (1 for “security” dice, 2 for “normal” dice and 3 for “risky”)
    """
    
    if (curPos == nSquares-1) :
        return nSquares-1, False
    
    if (prison):
        return curPos, False

    listDiceResults = [i for i in range(diceChoice+1)]
    result = random.choice(listDiceResults)

    if (curPos == 2 & result !=0) :
        slowLane = random.choice([0,1])
        if slowLane :
            newPos = curPos + result
        else :
            newPos = curPos + result + 7

    elif (curPos == 9 & result != 0):
        newPos = curPos + result + 5

    else : 
        newPos = curPos + result
    
    if (newPos > nSquares-1) :
        if (circle):
            newPos -= nSquares
        else :
            return nSquares-1, True
        
        
    newSquare = layout[newPos]

    if(diceChoice == 1):
        return newPos, False

    if (diceChoice == 2):
        newSquare = random.choice([0,newSquare])

    match newSquare : 

        case 0:
            return newPos, False  # nothing happens

        case 1 :
            return 1, False #back to square one

        case 2 : 
            if (newPos - 3 < 1): 
                return 1, False #back to square one
            return newPos - 3, False # back 3 squares

        case 3 : 
            return newPos, True #prison

        case 4 : 
            newSquare = random.choice([1,2,3])

            match newSquare : 

                case 1:
                    return 1, False  # back to square one

                case 2 : 
                    if (newPos - 3 < 1): 
                        return 1, False #back to square one
                    return newPos - 3, False # back 3 squares

                case 3 : 
                    return newPos, True #prison


def playOneGame(layout, circle):

    # start of the game

    curPos = 0 
    prison = False 

    if circle:

        while (curPos != nSquares-1):
            
            newPos, prison = playOneTurn(diceChoice=3,curPos=curPos, layout=layout, circle=circle, prison=prison)
            if (newPos > nSquares-1) :
                curPos = nSquares - newPos
            curPos = newPos
            print(curPos)

    if not circle : 

        while curPos < nSquares-1:
            
            newPos, prison = playOneTurn(diceChoice=3, curPos=curPos, layout=layout, circle=circle, prison=prison)
            curPos = newPos
            print(curPos)
                


#playOneGame([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], True)

val, dice = markovDecision([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], True)
print(val)
print(dice)
