#!/usr/bin/env python3

# https://adventofcode.com/2022/day/2

import sys

lines = sys.stdin.readlines()

opp_map = {
    'A': 1,  # rock
    'B': 2,  # paper
    'C': 3,  # scissors
}

total = 0
for line in lines:
    vals = line.split()
    opp = opp_map[vals[0]]
    you = vals[1]

    print(opp, you)

    score = 0

    if you == 'X':  # lose
        score += (opp - 2) % 3 + 1
        score += 0
    elif you == 'Y':  # draw
        score += opp
        score += 3
    elif you == 'Z':  # win
        score += (opp) % 3 + 1
        score += 6

    print(score)
    total += score

print(total)
