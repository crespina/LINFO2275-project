import random
import numpy as np
from part_I import markovDecision

nSquares = 15

def playOneTurn(diceChoice, curPos, layout, circle, prison):
    """
    The function playOneTurn simulates one turn of the game, given the choice of dice (1 for “security” dice, 2 for “normal” dice and 3 for “risky”)
    """

    if curPos == nSquares - 1:
        return nSquares - 1, False

    if prison:
        return curPos, False

    listDiceResults = [i for i in range(diceChoice + 1)]
    result = random.choice(listDiceResults)

    if curPos == 2 and result != 0:
        slowLane = random.choice([0, 1])
        if slowLane:
            newPos = curPos + result
        else:
            newPos = curPos + result + 7

    elif ((curPos == 9 and result != 0) or ( (curPos in [7,8,9]) and (curPos+result>=10))) :
        newPos = curPos + result + 4

    else:
        newPos = curPos + result

    if newPos > nSquares - 1:
        if circle:
            newPos -= nSquares
        else:
            return nSquares - 1, True

    newSquare = layout[newPos]

    if diceChoice == 1:
        return newPos, False

    elif diceChoice == 2:
        newSquare = random.choice([0, newSquare])

    match newSquare:

        case 0:
            return newPos, False  # nothing happens

        case 1:
            return 0, False  # back to square one

        case 2:
            if newPos - 3 < 0:
                return 0, False  # back to square one
            return newPos - 3, False  # back 3 squares

        case 3:
            return newPos, True  # prison

        case 4:
            newSquare = random.choice([1, 2, 3])

            match newSquare:

                case 1:
                    return 0, False  # back to square one

                case 2:
                    if newPos - 3 < 0:
                        return 0, False  # back to square one
                    return newPos - 3, False  # back 3 squares

                case 3:
                    return newPos, True  # prison


def playOneGame(layout, circle, policy):

    # start of the game
    nTurns = 0
    curPos = 0
    prison = False

    if circle:

        while curPos != nSquares - 1:

            newPos, prison = playOneTurn(
                diceChoice=policy[curPos], curPos=curPos, layout=layout, circle=circle, prison=prison
            )
            if newPos > nSquares - 1:
                curPos = nSquares - newPos
            curPos = newPos
            nTurns += 1

    else :

        while curPos < nSquares - 1:
            newPos, prison = playOneTurn(
                diceChoice=policy[curPos], curPos=curPos, layout=layout, circle=circle, prison=prison
            )
            curPos = newPos
            nTurns += 1
    return nTurns


def empirical_results(layout, circle, policy):

    avgnTurnsPlayed = 0

    for _ in range (1000) :
        nTurns = playOneGame(layout, circle, policy)
        avgnTurnsPlayed += nTurns / 1000

    return avgnTurnsPlayed

layout = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
circle = False
expec, dice = markovDecision(layout, circle)
dice = np.array([2, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1])

avgnTurns = empirical_results(layout, circle, dice.astype(int))
print(avgnTurns)
