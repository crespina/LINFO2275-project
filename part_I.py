import numpy as np
import random

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
    return

def playOneTurn(diceChoice, curPos, layout, circle):
    """
    The function playOneTurn simulates one turn of the game, given the choice of dice (1 for “security” dice, 2 for “normal” dice and 3 for “risky”)

    Args :

        diceChoice (int): - 1 : "security dice" = allows to move forward by 0 or 1 square, with a probability of 1/2, and ignoring the presence of traps
                          - 2 : "normal dice" = allows to move by 0, 1 or 2 squares with a probability of 1/3, and have a 50 % chance of triggering traps
                          - 3 : "risky dice" = allows to move by 0, 1, 2 or 3 squares with a probability of 1/4, and have a 100 % chance of triggering traps

        curPos (int): current position of the player on the layout of the game

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

        newPos (int): new position of the player on the layout of the game

        prison (bool): indicates if the player is now in prison, meaning that they cannot move on the next turn

    """

    listDiceResults = [i for i in range(diceChoice+1)]
    result = random.choice(listDiceResults)

    if ((curPos == 2) & (result !=0)) :
        slowLane = random.choice([0,1])
        if slowLane :
            newPos = curPos + result
        else :
            newPos = curPos + result + 7

    elif ((curPos == 9) & (result != 0)):
        newPos = curPos + result + 5

    else : 
        newPos = curPos + result

    if ((newPos == 14) | ((newPos > 14) & (not circle))) :
        return 14, False

    if circle :
        if newPos > 14:
            curPos = 15 - newPos

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
    """
    The function playOneGame simulates one entire game of Snakes & Ladders

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
        ? 

    """

    # start of the game

    curPos = 0 
    prison = False 
    numberOfTurnPlayed = 0

    if circle:

        while (curPos != 14): #needs to arrive perfectly on the goal square
            print(curPos)
            if not prison :
                newPos, prison = playOneTurn(diceChoice=1,curPos=curPos, layout=layout, circle=circle)
                curPos = newPos
            else : 
                prison = False

            numberOfTurnPlayed += 1

        print("goal")

    if not circle : 

        while curPos < 14: #doesnt need to arrive perfectly on the goal square
            print(curPos)
            if not prison:
                newPos, prison = playOneTurn(diceChoice=1, curPos=curPos, layout=layout, circle=circle)
                curPos = newPos
            else : 
                prison = False

            numberOfTurnPlayed += 1

        print("goal")


playOneGame([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], False)
