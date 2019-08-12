#!/usr/local/bin/python3
import sys
import numpy
import math
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

while True:
    try:
        score = float(input("\nEnter current score: "))
        if score >= 0:
            break
        else:
            print("\nCannot have a negative score. Please try again")
    except (TypeError, ValueError, NameError):
        print("\nValue for score is invalid. Please try again")

while 1:
    while 1:
        try:
            n_played = float(input("\nThe number of games played: "))
            break
        except (TypeError, ValueError, NameError):
            print("\nValue for number of games played is invalid. Please try again")
    if n_played < 0:
        print("\nCannot have a negative number of games. Please try again")
    elif n_played == 0:
        print("\nSorry you must have played at least one game to use this.", \
            "Please try again")
    else:
        break

if score > n_played:
    print("\nNot possible to have won more than you have played!\n")
    sys.exit()

current_ratio = score / n_played
print("\nCurrent ratio is", current_ratio)

while 1:
    while 1:
        try:
            target_ratio = float(input("\nWhat is the target ratio: "))
            break
        except (TypeError, ValueError, NameError):
            print("\nValue for ratio is invalid. Please try again")
    if target_ratio < 0:
        print("\nCannot have a negative ratio. Please try again")
    elif target_ratio > 1:
        print("\nCannot have a ratio greater than 1. Please try again")
    elif target_ratio == 1 and score != n_played:
        print("\nThis is not possible. Please try again")
    elif target_ratio == 0 and score != 0:
        print("\nThis is not possible. Please try again")
    else:
        break

w = int(0)
l = int(0)


def reach_ratio(target_ratio, score, n_played, w, l):
    if (score / n_played) == target_ratio:
        print("\nYou are on your target ratio \n")

    elif target_ratio > (score / n_played):
        while target_ratio > (score / n_played):
            score += 1
            n_played += 1
            w += 1
        print("\nThe number of games you need to win is", w)

    elif (score / n_played) > target_ratio:
        while (score / n_played) > target_ratio:
            n_played += 1
            l += 1
        print("\nThe number of games you need to lose is", l)


# exact answers to the number of games
# when target_ratio > (score / n_played) and x is additional number of games to win
# solve (score + x) / (n_played + x) >= target_ratio for x
# when (score / n_played) > target_ratio and y is additional number of games you lose
# solve target_ratio >= score / (n_played + y) for y
# Was careful and make sure x and y are on the greater than side

def exact_games(target_ratio, score, n_played):
    if (score / n_played) == target_ratio:
        return
    elif target_ratio > (score / n_played):
        x = ((target_ratio * n_played) - score) / (1 - target_ratio)
        print("\nExact number of games to win to reach target ratio is", x)

    elif (score / n_played) > target_ratio:
        y = (score - (target_ratio * n_played)) / target_ratio
        print("\nExact number of games to lose to reach target ratio is", y)


reach_ratio(target_ratio, score, n_played, w, l)
exact_games(target_ratio, score, n_played)


# New feature provides next few ratios

def next_ratios(score, n_played):
    print("\nNext feature. Say the state (win or lose) and the number of games", \
        "and it tells you the ratios in that state for those number of games. Typing", \
        "anything other than w or l means you decide not to use the feature.")
    while 1:
        w_or_l = input("\nAre you going to win or lose the next games. w or l: ")
        if w_or_l == "w" or w_or_l == "W" or w_or_l == "l" or w_or_l == "L":
            break
        else:
            print("\nDecided not to use next ratio feature")
            return
    while 1:
        while 1:
            try:
                # games is an integer to work with a for loop
                games = int(input("\nThe number of these games played: "))
                break
            except (TypeError, ValueError, NameError):
                print("\nValue for number of games played is invalid. Please try again")
        if games < 0:
            print("\nCannot have a negative number of games. Please try again")
        elif games == 0:
            print("\nSorry you must have played at least one game to use this.", \
                "Please try again")
        else:
            break

    if w_or_l == "w" or w_or_l == "W":
        print("\nRatio for the next", games, "games are")
        for x in range(0, games):
            score += 1
            n_played += 1
            r_1 = (score / n_played)
            print(r_1)

    elif w_or_l == "l" or w_or_l == "L":
        print("\nRatio for the next", games, "games are")
        for x in range(0, games):
            n_played += 1
            r_2 = (score / n_played)
            print(r_2)


next_ratios(score, n_played)

# need to use these so can reset them after loop below
score_p = score
n_played_p = n_played


# from proportion of wins calculate average number of games to reach target rato
# over time games will tend to the given proportion so this propotion will only
# work if there is a 0.05 difference between proportion and target ratio
# going up to a target ratio, proportion of wins needs to be atleast 0.05 higher
# going down to target rato, proportion of wins needs to be atleast 0.05 lower
# chose 0.05 as found if they are too similar it sometimes never solves and
# leads to an endless loop

def proportion_wins(target_ratio, score, n_played, score_p, n_played_p):
    if (score / n_played) == target_ratio:
        print("\nProportion feature does not apply when you are on your target ratio")
        return
    # due to the 0.05 difference required target ratio cannot be below 0.05 or above 0.95
    if target_ratio < 0.05 or target_ratio > 0.95:
        print("\nProportion feature only works if target ratio is between 0.05 and 0.95")
        return

    if target_ratio > (score / n_played):
        print("\nNext feature. Provide a proportion of expected wins and using", \
            "the bernoulli distrubution will calculate the number of games to get up", \
            "to the target ratio. So the caclulation does not take a long time", \
            "to calculate and is reasonably possible will only calculate if the", \
            "proportion is 0.05 higher than target ratio,", target_ratio)

        while 1:
            while 1:
                try:
                    pr = float(input("\nProportion of games expected to win: "))
                    break
                except (TypeError, ValueError, NameError):
                    print("\nValue for proportion is invalid. Please try again")
            if pr < 0:
                print("\nSorry cannot have a proportion less than 0")
            elif pr > 1:
                print("\nSorry cannot have a proportion greater than 1")
            elif (pr - target_ratio) < 0.049:
                print("\nSorry proportion must be at least 0.05 higher than your", \
                    "target ratio", target_ratio, ", please try again")
            else:
                break

        games_until_ratio = []
        g = int(0)
        # s is bernouilli version of binomial(n=1), gives out 1 or 0 (win or loss) randomly
        # to an expected propirtion of wins = pr. Add win or lose to score and game played
        # keep track of games played, g, and see how many needed to reach target ratio
        # repeat 10,000 times and average to work out average g to reach target ratio
        for x in range(0, 10000):
            while target_ratio > (score_p / n_played_p):
                g += 1
                s = numpy.random.binomial(size=1, n=1, p=pr)
                for x in s:
                    if s[0] == 1:
                        score_p += 1
                        n_played_p += 1
                    elif s[0] == 0:
                        n_played_p += 1
            games_until_ratio.append(g)
            # need to reset the score and n_played or will remain constant in array
            score_p = score
            n_played_p = n_played
            g = int(0)
        av = float(sum(games_until_ratio)) / float(len(games_until_ratio))
        print("\nAverage number of games needed to reach target ratio is", av)
        av = int(numpy.ceil(av))
        print("\nSo averagely you need to play", av, "games to reach your target ratio")

    elif (score_p / n_played_p) > target_ratio:
        print("\nNext feature. Provide a proportion of expected wins and using", \
            "the bernoulli distrubution will calculate the number of games to get down", \
            "to the target ratio. So the caclulation does not take a long time", \
            "to calculate and is reasonably possible will only calculate if the", \
            "proportion is 0.05 lower than target ratio,", target_ratio)

        while 1:
            while 1:
                try:
                    pr = float(input("\nProportion of games expected to win: "))
                    break
                except (TypeError, ValueError, NameError):
                    print("\nValue for proportion is invalid. Please try again")
            if pr < 0:
                print("\nSorry cannot have a proportion less than 0. Please try again.")
            elif pr > 1:
                print("\nSorry cannot have a proportion greater than 1. Please try again.")
            elif (target_ratio - pr) < 0.049:
                print("\nSorry proportion must be at least 0.05 lower than your", \
                    "target ratio", target_ratio, ", please try again")
            else:
                break
        games_until_ratio = []
        g = int(0)
        # same as before but down to target ratio
        for x in range(0, 10000):
            while (score_p / n_played_p) > target_ratio:
                g += 1
                s = numpy.random.binomial(size=1, n=1, p=pr)
                for x in s:
                    if s[0] == 1:
                        score_p += 1
                        n_played_p += 1
                    elif s[0] == 0:
                        n_played_p += 1
            games_until_ratio.append(g)
            score_p = score
            n_played_p = n_played
            g = int(0)
        av = float(sum(games_until_ratio)) / float(len(games_until_ratio))
        print ("\nAverage number of games needed to reach target ratio is", av)
        av = int(numpy.ceil(av))
        print("\nSo averagely you need to play", av, "games to reach your target ratio")


proportion_wins(target_ratio, score, n_played, score_p, n_played_p)


# round up or down to the nearest a; for me 0.05 to make expected proportions nice
def round_up(x, a):
    return (math.ceil(x / a) * a)


def round_down(x, a):
    return (math.floor(x / a) * a)


print("\nFinal feature gives you the number of games you need to play to reach", \
    "the target ratio for different expected proportions of wins. ", \
    "Then constructs a graph of this")


# skeleton of previous definition

def proportion_wins_2(pr, target_ratio, score, n_played, score_p, n_played_p):
    if target_ratio > (score / n_played):
        games_until_ratio = []
        g = int(0)
        for x in range(0, 10000):
            while target_ratio > (score_p / n_played_p):
                g += 1
                s = numpy.random.binomial(size=1, n=1, p=pr)
                for x in s:
                    if s[0] == 1:
                        score_p += 1
                        n_played_p += 1
                    elif s[0] == 0:
                        n_played_p += 1
            games_until_ratio.append(g)
            score_p = score
            n_played_p = n_played
            g = int(0)
        av = float(sum(games_until_ratio)) / float(len(games_until_ratio))
        return av

    elif (score_p / n_played_p) > target_ratio:
        games_until_ratio = []
        g = int(0)
        for x in range(0, 10000):
            while (score_p / n_played_p) > target_ratio:
                g += 1
                s = numpy.random.binomial(size=1, n=1, p=pr)
                for x in s:
                    if s[0] == 1:
                        score_p += 1
                        n_played_p += 1
                    elif s[0] == 0:
                        n_played_p += 1
            games_until_ratio.append(g)
            score_p = score
            n_played_p = n_played
            g = int(0)
        av = float(sum(games_until_ratio)) / float(len(games_until_ratio))
        return av


def iteration_proportion_wins(target_ratio, score, n_played, score_p, n_played_p):
    if (score / n_played) == target_ratio:
        print("\nProportion feature does not apply when you are on your target ratio")
        return
    # due to the 0.05 difference required target ratio cannot be below 0.05 or above 0.95
    if target_ratio < 0.05 or target_ratio > 0.95:
        print("\nProportion feature only works if target ratio is between 0.05 and 0.95")
        return
    print("\nThis feature takes a few minutes, would you like to continue? y to continue.", \
        "Anything else means you have decided not to use it")

    while 1:
        y = input("\nWould you like to continue, y? ")
        if y == "y" or y == "Y" or y == "y " or y == "Y ":
            break
        else:
            print("\nDecided not to use this feature")
            return

    if target_ratio > (score / n_played):
        # round target ratio to nearest 0.05
        print("\nFollowing are for a target ratio of", target_ratio)
        # only works if expected wins is 0.05 higher
        pr = round_up((target_ratio + 0.05), 0.05)
        pr_array = []
        games_array = []
        # iterate through all of the different expected wins of 0.05 apart to find
        # number of games required
        while pr <= 1:
            pr = round(pr, 2)
            pr_array.append(pr)
            g_a = proportion_wins_2(pr, target_ratio, score, n_played, score_p, n_played_p)
            games_array.append(g_a)
            pr += 0.05
        # print them all out
        for x in range(len(pr_array)):
            print("\nExpected proportion of wins:", pr_array[x])
            print("Number of games to reach target ratio:", math.ceil(games_array[x]))
        pr = round_up((target_ratio + 0.05), 0.05)
        # reset to do again with 0.01 difference for the graph
        pr_array_01 = []
        games_array_01 = []
        while pr <= 1:
            pr = round(pr, 2)
            pr_array_01.append(pr)
            g_a = proportion_wins_2(pr, target_ratio, score, n_played, score_p, n_played_p)
            games_array_01.append(g_a)
            pr += 0.01
        print("\nGraph of numer of games to reach", \
            " target ratio,", target_ratio, ",for different expected proportion of wins")
        plt.plot(pr_array_01, games_array_01)
        plt.xlabel("Expected proportion of wins")
        plt.ylabel("Number of games to reach target ratio")
        target_ratio = target_ratio
        plt.title('Target ratio: %s' % target_ratio)
        plt.show()

    elif (score_p / n_played_p) > target_ratio:
        # round target ratio to nearest 0.05
        print("\nFollowing are for a target ratio of", target_ratio)
        pr = round_down((target_ratio - 0.05), 0.05)
        pr_array = []
        games_array = []
        while pr >= 0:
            pr = round(pr, 2)
            pr_array.append(pr)
            g_a = proportion_wins_2(pr, target_ratio, score, n_played, score_p, n_played_p)
            games_array.append(g_a)
            pr -= 0.05
        for x in range(len(pr_array)):
            print("\nExpected proportion of wins:", pr_array[x])
            print("Number of games to reach target ratio:", math.ceil(games_array[x]))
        pr = round_down((target_ratio - 0.05), 0.05)
        pr_array_01 = []
        games_array_01 = []
        while pr >= 0:
            pr = round(pr, 2)
            pr_array_01.append(pr)
            g_a = proportion_wins_2(pr, target_ratio, score, n_played, score_p, n_played_p)
            games_array_01.append(g_a)
            pr -= 0.01
        print("\nGraph of numer of games to reach", \
            " target ratio,", target_ratio, ",for different expected proportion of wins")
        plt.plot(pr_array_01, games_array_01)
        plt.xlabel("Expected proportion of wins")
        plt.ylabel("Number of games to reach target ratio")
        target_ratio = target_ratio
        plt.title('Target ratio: %s' % target_ratio)
        plt.show()


iteration_proportion_wins(target_ratio, score, n_played, score_p, n_played_p)
