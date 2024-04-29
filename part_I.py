import numpy as np
import random
import copy
from proba import proba_security_dice, proba_normal_dice, proba_risky_dice

nSquares = 15
precision = 1e-9

"""
 [0, 0, 0, 0, 0, 3, 0, 0, 0, 3, 0, 3, 0, 0, 0]
layout : 
___________________________________________________________________
|  0  |  1  |  2  |  3  |  4  |  5P  |  6  |  7  |  8  |  9P  |  14  |
|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|______|
              \                                                / 
               \                                              /   
           _____\____________________________________________/____
          |    10      |      11  P    |      12      |     13     |
          |____________|______________|______________|____________|                    


"""


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
    proba_security = proba_security_dice()
    proba_normal, prison_normal = proba_normal_dice(layout,circle)
    proba_risky, prison_risky = proba_risky_dice(layout,circle)

    value = np.zeros(nSquares)
    newValue = np.array([8.5,7.5,6.5,7,6,5,4,3,2,1,4,3,2,1,0])

    while (sum(abs(newValue-value)) > precision):
        value = copy.deepcopy(newValue)
        for i in range (nSquares-1):
            newValue[i] = 1 + min(
                np.dot(proba_security[i], value),
                np.dot(proba_normal[i], value) + sum(prison_normal[i]),
                np.dot(proba_risky[i], value)+ sum(prison_risky[i])
            )
        newValue[nSquares-1] = min(np.dot(proba_security[nSquares-1],value), np.dot(proba_normal[nSquares-1],value), np.dot(proba_risky[nSquares-1],value))

    dice = np.zeros(15, dtype=float)
    for i in range (nSquares):
        dice[i] = np.argmin(
            [
                np.dot(proba_security[i], newValue),
                np.dot(proba_normal[i], newValue) + sum(prison_normal[i]),
                np.dot(proba_risky[i], newValue) + sum(prison_risky[i]),
            ]
        )

    return newValue, dice + 1


layout = [0, 0, 0, 0, 0, 3, 0, 0, 0, 3, 0, 3, 0, 0, 0]
circle = False
_, optimal_policy = markovDecision(layout, circle)
