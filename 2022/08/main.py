#!/usr/bin/env python3

import sys
import numpy as np


# Parse grid

grid = []
for line in sys.stdin:
    row = []
    for c in line.strip():
        row.append(int(c))
    grid.append(row)

grid = np.array(grid)

print(grid)

# Count visible trees


def visible(i, j):
    global grid
    height = grid[i][j]
    views = [
        grid[i, j+1:],  # left
        grid[i, :j],  # right
        grid[:i, j],  # up
        grid[i+1:, j],  # down
    ]
    for view in views:
        #  print(f"{i}x{j}: {view}")
        if len(view) == 0 or max(view) < height:
            return True
    return False


visible_count = 0

for i, row in enumerate(grid):
    for j, tree in enumerate(row):
        if visible(i, j):
            visible_count += 1

print('visible trees:', visible_count)
