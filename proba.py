import numpy as np

nSquares = 15

def proba_security_dice():
    """
    The function proba_security_dice computes, for every pair of squares in the game (i,j) the theoretical probability to go from square i to square j using the security dice

    Args :

    Returns :

        Proba (numpy.ndarray[nSquares][nSquares]):  Matrix containing the probability : proba[i][j] gives the probability of going from square i to square j

    """

    proba = np.zeros((nSquares, nSquares))

    for i in range(nSquares - 1):

        # 1 chance out of 2 to stay at the same place
        proba[i][i] = 0.5

        # 1 chance out of 2 to go 1 further
        if i == 2:
            proba[i][i + 1] = 0.25  # slow lane
            proba[i][i + 8] = 0.25  # fast lane

        elif i == 9:
            proba[i][i + 5] = 0.5

        else:
            proba[i][i + 1] = 0.5

    proba[nSquares - 1][nSquares - 1] = 1  # the end
    return proba


def proba_normal_dice(layout, circle):

    """
    The function proba_normal_dice computes, for every pair of squares in the game (i,j) the theoretical probability to go from square i to square j using the normal dice

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

        proba (numpy.ndarray[nSquares][nSquares]):  Matrix containing the probability : proba[i][j] gives the probability of going from square i to square j

        proba_prison (numpy.ndarray[nSquares][nSquares]): Matrix containing the probability of ending up in prison : proba_prison[i][j] gives the probability of skipping next turn if going from square i to square j

    """

    proba = np.zeros((nSquares, nSquares))
    proba_prison = np.zeros((nSquares, nSquares))
    for i in range(nSquares - 1):

        # 1 chance out of 3 to stay at the same place
        proba[i][i] = 1 / 3

        # 1 chance out of 3 to go 1 further
        # 1 chance out of 3 to go 2 further

        if i == 2:
            proba[i][i + 1] = 1 / 6  # slow lane
            proba[i][i + 2] = 1 / 6  # slow lane
            proba[i][i + 8] = 1 / 6  # fast lane
            proba[i][i + 9] = 1 / 6  # fast lane

        elif i == 8:
            proba[i][i + 1] = 1 / 3
            proba[i][i + 6] = 1 / 3

        elif i == 9:
            if circle:
                proba[i][i + 5] = 1 / 3
                proba[i][0] = 1 / 3
            else:
                proba[i][i + 5] = 2 / 3

        elif i == 13:
            if circle:
                proba[i][i + 1] = 1 / 3
                proba[i][0] = 1 / 3
            else:
                proba[i][i + 1] = 2 / 3

        else:
            proba[i][i + 1] = 1 / 3
            proba[i][i + 2] = 1 / 3

        # traps

    for i in range(nSquares - 1):
        for j in range(nSquares - 1):

            match layout[j]:

                case 1:  # restart
                    if j != 0:
                        proba[i][0] += proba[i][j] / 2
                        proba[i][j] /= 2

                case 2:  # penalty
                    proba[i][j - 3 if j - 3 >= 0 else 0] += proba[i][j] / 2
                    proba[i][j] /= 2

                case 3:  # prison
                    proba_prison[i][j] = proba[i][j] / 2

                case 4:  # mystery

                    # if j != 0:
                    proba[i][0] += proba[i][j] / 6  # trap restart

                    proba[i][j - 3 if j - 3 >= 0 else 0] += proba[i][j] / 6 # trap minus 3

                    proba_prison[i][j] += proba[i][j] / 6  # trap prison

                    proba[i][j] *= 4 / 6  # don't activate the trap + prison

    proba[nSquares - 1][nSquares - 1] = 1

    return proba, proba_prison


def proba_risky_dice(layout, circle):

    """
    The function proba_risky_dice computes, for every pair of squares in the game (i,j) the theoretical probability to go from square i to square j using the risky dice

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

        proba (numpy.ndarray[nSquares][nSquares]):  Matrix containing the probability : proba[i][j] gives the probability of going from square i to square j

        proba_prison (numpy.ndarray[nSquares][nSquares]): Matrix containing the probability of ending up in prison : proba_prison[i][j] gives the probability of skipping next turn if going from square i to square j

    """

    proba = np.zeros((nSquares, nSquares))
    proba_prison = np.zeros((nSquares, nSquares))
    for i in range(nSquares - 1):

        # 1 chance out of 4 to stay at the same place
        proba[i][i] = 1 / 4

        # 1 chance out of 4 to go 1 further
        # 1 chance out of 4 to go 2 further
        # 1 chance out of 4 to go 3 further

        if i == 2:
            proba[i][i + 1] = 1 / 8  # slow lane
            proba[i][i + 2] = 1 / 8  # slow lane
            proba[i][i + 3] = 1 / 8  # slow lane

            proba[i][i + 8] = 1 / 8  # fast lane
            proba[i][i + 9] = 1 / 8  # fast lane
            proba[i][i + 10] = 1 / 8  # fast lane

        elif i == 7:
            proba[i][i + 1] = 1 / 4
            proba[i][i + 2] = 1 / 4
            proba[i][i + 7] = 1 / 4

        elif i == 8:
            if circle:
                proba[i][i + 1] = 1 / 4
                proba[i][i + 6] = 1 / 4
                proba[i][0] = 1 / 4
            else:
                proba[i][i + 1] = 1 / 4
                proba[i][i + 6] = 1 / 2

        elif i == 9:
            if circle:
                proba[i][i + 5] = 1 / 4
                proba[i][0] = 1 / 4
                proba[i][1] = 1 / 4
            else:
                proba[i][i + 5] = 3 / 4

        elif i == 12:
            if circle:
                proba[i][i + 1] = 1 / 4
                proba[i][(i + 2)] = 1 / 4
                proba[i][0] = 1 / 4
            else:
                proba[i][i + 1] = 1 / 4
                proba[i][i + 2] = 1 / 2

        elif i == 13:
            if circle:
                proba[i][i + 1] = 1 / 4
                proba[i][0] = 1 / 4
                proba[i][1] = 1 / 4
            else:
                proba[i][nSquares - 1] = 3 / 4

        else:
            proba[i][i + 1] = 1 / 4
            proba[i][i + 2] = 1 / 4
            proba[i][i + 3] = 1 / 4

    # traps

    for i in range(nSquares - 1):
        for j in range(nSquares - 1):

            match layout[j]:

                case 1:  # restart
                    if j != 0:
                        proba[i][0] += proba[i][j]
                        proba[i][j] = 0

                case 2:  # penalty
                    proba[i][j - 3 if j - 3 >= 0 else 0] += proba[i][j]
                    proba[i][j] = 0

                case 3:  # prison
                    proba_prison[i][j] = proba[i][j]

                case 4:  # mystery : 1 out of 3 traps

                    if j != 0:
                        proba[i][0] += proba[i][j] / 3  # trap restart

                    proba[i][j - 3 if j - 3 >= 0 else 0] += proba[i][j] / 3 # trap minus 3

                    proba_prison[i][j] += proba[i][j] / 3  # trap prison
                    
                    proba[i][j] /= 3

    proba[nSquares - 1][nSquares - 1] = 1

    return proba, proba_prison
