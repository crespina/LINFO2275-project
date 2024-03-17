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
