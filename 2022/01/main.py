#!/usr/bin/env python3

# https://adventofcode.com/2022/day/1

import sys

acc = []
elves = []

lines = sys.stdin.readlines()
for line in [l.strip() for l in lines]:
    if line == '':
        elves.append(acc)
        acc = []
        continue
    acc.append(int(line))

sums = [sum(elf) for elf in elves]
sums.sort()

print(f'max: {sums[-1]}')

top3 = sums[-3:]

print(f'top 3 sum: {sum(top3)}')
