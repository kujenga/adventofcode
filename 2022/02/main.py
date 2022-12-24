#!/usr/bin/env python3

# https://adventofcode.com/2022/day/2

import sys

lines = sys.stdin.readlines()

opp_map = {
    'A': 1,
    'B': 2,
    'C': 3,
}

you_map = {
    'X': 1,
    'Y': 2,
    'Z': 3,
}

total = 0
for line in lines:
    vals = line.split()
    opp = opp_map[vals[0]]
    you = you_map[vals[1]]

    score = you

    if opp == you:
        score += 3
    elif opp == 1 and you == 2:
        score += 6
    elif opp == 2 and you == 3:
        score += 6
    elif opp == 3 and you == 1:
        score += 6

    total += score

print(total)
