#!/usr/bin/env python3

import sys
import numpy as np
from PIL import Image

np.set_printoptions(threshold=sys.maxsize, linewidth=sys.maxsize)

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
#  print(rocks)

# Setup cave
ROCK = 255
FLOOR = 200
SAND = 100
dim = 750
cave = np.zeros([dim, dim], dtype=np.uint8)  # big enough
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
# Draw floor
locations = np.argwhere(cave)
max_depth = np.amax(locations, axis=0)[1]
print('max rock depth:', max_depth)
cave[:, max_depth+2] = FLOOR

#  print(cave)

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
            if grains % 1000 == 0:
                print(f"sand grain {grains} landed at {grain}")
                Image.fromarray(cave.transpose()).save('cave.png')
            grains += 1
            cave[grain] = SAND
            if grain == sand_origin:
                print('found origin!')
                filling = False
            break
        # Sand reached the floor, log a message for part 1.
        if cave[n] == FLOOR:
            print(f"floor reached at {grains} grains")
        grain = n

print('grains total:', grains)
