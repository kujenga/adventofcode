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

total = 0
for i in range(0, int(len(lines)/3)):
    a = set(lines[i*3+0])
    b = set(lines[i*3+1])
    c = set(lines[i*3+2])

    badge = a.intersection(b, c).pop()
    total += val(badge)

print(total)
