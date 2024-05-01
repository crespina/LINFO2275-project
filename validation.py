import random
import numpy as np
import matplotlib.pyplot as plt
from part_I import markovDecision

nSquares = 15
nSimul = 20_000

###############################################################################
###############################################################################
############################### PLAY THE GAME #################################
###############################################################################
###############################################################################

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


def playOneGame(layout, circle, policy, start=0):

    # start of the game
    nTurns = 0
    curPos = start
    prison = False
    
    #i thought this was the problem but it doesnt make sense that the expected cost of square 0 be impacted by that
    """
    if (layout[start] == 3):
        if (policy[start] == 3):
            prison = True
        if (policy[start] == 2):
            prison = random.choice([True,False])
    """
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


###############################################################################
###############################################################################
################################ COMPARISONS ##################################
###############################################################################
###############################################################################

def empiric_cost_of_square(layout, circle, policy, nSimul):

    expected_costs = np.zeros(nSquares)

    for start_square in range(nSquares):

        total_turns = 0
        for _ in range(nSimul):
            total_turns += playOneGame(layout, circle, policy, start=start_square)

        expected_costs[start_square] = total_turns / nSimul

    return expected_costs

def empirical_results(layout, circle, policy):

    avgnTurnsPlayed = 0

    for _ in range (nSimul) :
        nTurns = playOneGame(layout, circle, policy)
        avgnTurnsPlayed += nTurns

    return avgnTurnsPlayed / nSimul


def comparison_theorical_empirical(layout, circle):

    expec, optimal_policy = markovDecision(layout, circle)
    actual = empiric_cost_of_square(layout, circle, optimal_policy.astype(int), nSimul)
    expec = np.append(expec,0)

    print(optimal_policy)

    # Generating x-axis values (squares)
    squares = np.arange(len(expec))

    # Plotting both arrays on the same plot
    plt.plot(squares, expec, label="Theoretical cost")
    plt.plot(squares, actual, label="Empirical cost")

    plt.xticks(np.arange(0, len(expec), step=1))

    # Adding grid and labels
    plt.grid(True)
    plt.xlabel("Square")
    plt.ylabel("Cost")

    # Adding legend
    plt.legend()
    plt.title("Comparison between the expected cost and the actual cost")

    # Displaying the plot
    plt.show()


def comparison_theorical_empirical_multiple_simul(layout, circle):

    expec, optimal_policy = markovDecision(layout, circle)
    expec = np.append(expec, 0)
    actual = []
    nSimuls = [10,100,1000,10000]
    for nSimul in nSimuls:
        actual.append(empiric_cost_of_square(layout,circle,optimal_policy.astype(int),nSimul))

    print(optimal_policy)

    # Generating x-axis values (squares)
    squares = np.arange(len(expec))

    # Plotting both arrays on the same plot
    plt.plot(squares, expec, label="Theoretical cost")
    plt.plot(squares, actual[0], label="Empirical cost with 10 simulations")
    plt.plot(squares, actual[1], label="Empirical cost with 100 simulations")
    plt.plot(squares, actual[2], label="Empirical cost with 1000 simulations")
    plt.plot(squares, actual[3], label="Empirical cost with 10000 simulations")

    plt.xticks(np.arange(0, len(expec), step=1))

    # Adding grid and labels
    plt.grid(True)
    plt.xlabel("Square")
    plt.ylabel("Cost")

    # Adding legend
    plt.legend()
    plt.title("Comparison between the expected cost and the actual cost")

    # Displaying the plot
    plt.show()


def comparison_theorical_empirical_loss_square(layout, circle):

    expec, optimal_policy = markovDecision(layout, circle)
    expec = np.append(expec, 0)
    actual = []
    nSimuls = [10, 100, 1000, 10000]
    for nSimul in nSimuls:
        actual.append(
            empiric_cost_of_square(layout, circle, optimal_policy.astype(int), nSimul)
        )

    print(optimal_policy)

    # Generating x-axis values (squares)
    squares = np.arange(len(expec))

    # Plotting both arrays on the same plot
    plt.plot(squares, abs(expec - actual[0]), label="Loss with 10 simulations")
    plt.plot(squares, abs(expec - actual[1]), label="Loss with 100 simulations")
    plt.plot(squares, abs(expec - actual[2]), label="Loss with 1000 simulations")
    plt.plot(squares, abs(expec - actual[3]), label="Loss with 10000 simulations")

    plt.xticks(np.arange(0, len(expec), step=1))

    # Adding grid and labels
    plt.grid(True)
    plt.xlabel("Square")
    plt.ylabel("Loss")

    # Adding legend
    plt.legend()
    plt.title("Loss over different number of games played")

    # Displaying the plot
    plt.show()


def comparison_theorical_empirical_loss_total(layout, circle):

    expec, optimal_policy = markovDecision(layout, circle)
    expec = np.append(expec, 0)
    actual = []
    nSimuls = [10, 100, 1000, 10000, 100000]
    for nSimul in nSimuls:
        actual.append(
            empiric_cost_of_square(layout, circle, optimal_policy.astype(int), nSimul)
        )

    print(optimal_policy)

    names = ["10", "100", "1000", "10 000", "100 000"]
    loss = []
    loss.append(abs(sum(expec) - sum(actual[0])))
    loss.append(abs(sum(expec) - sum(actual[1])))
    loss.append(abs(sum(expec) - sum(actual[2])))
    loss.append(abs(sum(expec) - sum(actual[3])))
    loss.append(abs(sum(expec) - sum(actual[4])))

    plt.bar(names, loss)

    plt.xlabel("Number of simulations")
    plt.ylabel("Total Loss")

    # Adding legend
    plt.legend()
    plt.title("Loss over different number of games played")

    # Displaying the plot
    plt.show()


def comparison_of_policies_total(layout, circle):

    policies = []

    _, optimal_policy = markovDecision(layout, circle)
    policies.append(optimal_policy.astype(int))

    only_dice_risky = np.ones(nSquares, dtype=int)*3
    only_dice_normal = np.ones(nSquares, dtype=int) * 2
    only_dice_safe = np.ones(nSquares,dtype=int)
    rand = np.zeros(nSquares, dtype=int)
    for i in range(nSquares-1):
        rand[i] = random.choice([1,2,3])

    policies.append(only_dice_safe)
    policies.append(only_dice_normal)
    policies.append(only_dice_risky)
    policies.append(rand)
    policies.append([2, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3])

    avgnTurns = []

    for policy in policies:
        avgnTurns.append(empirical_results(layout, circle, policy))

    names = ["optimal", "safe", "normal", "risky", "random", "custom"]

    # Creating the bar plot
    plt.bar(names, avgnTurns)

    # Adding labels and title
    plt.xlabel("Policy")
    plt.ylabel("Cost")
    plt.title("Expected number of turns by policy")

    # Displaying the plot
    plt.show()


def comparison_of_policies_squares(layout, circle):

    policies = []

    _, optimal_policy = markovDecision(layout, circle)
    policies.append(optimal_policy.astype(int))

    only_dice_risky = np.ones(nSquares, dtype=int) * 3
    only_dice_normal = np.ones(nSquares, dtype=int) * 2
    only_dice_safe = np.ones(nSquares, dtype=int)
    rand = np.zeros(nSquares, dtype=int)
    for i in range(nSquares - 1):
        rand[i] = random.choice([1, 2, 3])

    policies.append(only_dice_safe)
    policies.append(only_dice_normal)
    policies.append(only_dice_risky)
    policies.append(rand)
    policies.append([2,1,3,3,3,3,3,3,3,3,3,3,3,3,3])

    avgnTurns = []

    for policy in policies:
        avgnTurns.append(empiric_cost_of_square(layout, circle, policy, nSimul))

    # Generating x-axis values (squares)
    squares = np.arange(len(avgnTurns[0]))

    # Plotting both arrays on the same plot
    plt.plot(squares, avgnTurns[0], label="Optimal")
    plt.plot(squares, avgnTurns[1], label="Safe")
    plt.plot(squares, avgnTurns[2], label="Normal")
    plt.plot(squares, avgnTurns[3], label="Risky")
    plt.plot(squares, avgnTurns[4], label="Random")
    plt.plot(squares, avgnTurns[5], label="Custom")

    plt.xticks(np.arange(0, len(avgnTurns[0]), step=1))

    # Adding grid and labels
    plt.grid(True)
    plt.xlabel("Square")
    plt.ylabel("Cost")

    # Adding legend
    plt.legend()
    plt.title("Expected cost for different policies")

    # Displaying the plot
    plt.show()

###############################################################################
###############################################################################
################################## PLOTS ######################################
###############################################################################
###############################################################################

def make_plots_results() :

    layout = [0, 0, 4, 0, 4, 0, 2, 1, 0, 0, 3, 0, 0, 3, 0]
    circle = False
    comparison_theorical_empirical(layout,circle)
    comparison_theorical_empirical_multiple_simul(layout,circle)
    comparison_theorical_empirical_loss_square(layout, circle)
    comparison_theorical_empirical_loss_total(layout, circle)


def make_plots_policies():
    layout = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    circle = False
    comparison_of_policies_total(layout,circle)
    comparison_of_policies_squares(layout, circle)

make_plots_policies()
