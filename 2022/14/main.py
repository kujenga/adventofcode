#!/usr/bin/env python3

import sys
import numpy as np

sand_origin = (500, 0)

# Parse rock outline paths.
rocks = []
for line in sys.stdin:
    path = []
    for point in line.strip().split('->'):
        point = point.strip()
        x, y = point.split(',')
        path.append([int(x), int(y)])
    rocks.append(path)
print(rocks)

# Setup cave
ROCK = 8
SAND = 1
dim = 750
cave = np.zeros([dim, dim], dtype=np.int8)  # big enough
for rock in rocks:
    for i, cur in enumerate(rock):
        if i == 0:
            continue
        # Fill in rocks
        prev = rock[i-1]
        xr = sorted([prev[0], cur[0]])
        yr = sorted([prev[1], cur[1]])
        for i in range(xr[0], xr[1]+1):
            for j in range(yr[0], yr[1]+1):
                cave[i, j] = ROCK

np.set_printoptions(threshold=sys.maxsize, linewidth=sys.maxsize)
print(cave)

# Simulate sand


def next_move(g):
    global cave

    down = (g[0], g[1] + 1)
    if cave[down] == 0:
        return down
    down_left = (g[0] - 1, g[1] + 1)
    if cave[down_left] == 0:
        return down_left
    down_right = (g[0] + 1, g[1] + 1)
    if cave[down_right] == 0:
        return down_right


grains = 0
filling = True
while filling:
    grain = sand_origin

    while filling:
        n = next_move(grain)
        #  print(f"sand grain moving from {grain} to {n}")
        if n is None:
            print(f"sand grain {grains} landed at {grain}")
            grains += 1
            cave[grain] = SAND
            break
        # Sand spilling out the bottom
        if n[1] >= dim-1:
            filling = False
        grain = n

print('grains total:', grains)
