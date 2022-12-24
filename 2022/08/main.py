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


def views(i, j):
    global grid
    return [
        np.flip(grid[i, :j]),  # left
        grid[i, j+1:],  # right, pointing away
        np.flip(grid[:i, j]),  # up, pointing away
        grid[i+1:, j],  # down
    ]


def visible(i, j):
    global grid
    height = grid[i][j]
    for view in views(i, j):
        #  print(f"{i}x{j}: {view}")
        if len(view) == 0 or max(view) < height:
            return True
    return False


def view_score(i, j):
    global grid
    height = grid[i][j]
    score = 1
    for view in views(i, j):
        view_dist = 0
        for v in view:
            view_dist += 1
            if v >= height:
                break
        score *= view_dist
    return score


visible_count = 0
view_scores = []

for i, row in enumerate(grid):
    for j, tree in enumerate(row):
        if visible(i, j):
            visible_count += 1
        view_scores.append(view_score(i, j))

#  view_score(3, 2)

print('visible trees:', visible_count)
print('max view score:', max(view_scores))
