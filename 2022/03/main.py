#!/usr/bin/env python3

import sys


# https://stackoverflow.com/a/4528997/2528719
def val(c):
    if c.islower():
        v = ord(c) - 96
    else:
        v = ord(c) - 38
    return v


assert val('a') == 1
assert val('z') == 26
assert val('A') == 27
assert val('Z') == 52


lines = [line.strip() for line in sys.stdin.readlines()]

compartments = [(l[:int(len(l)/2)], l[int(len(l)/2):]) for l in lines]

total = 0
for (a, b) in compartments:
    inter = set(a).intersection(set(b)).pop()
    total += val(inter)

print(total)
