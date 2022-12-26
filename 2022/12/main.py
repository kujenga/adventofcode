#!/usr/bin/env python3

import sys
import numpy as np
from pprint import pprint
from functools import total_ordering
import heapq

# parsing

grid = []
s = (None, None)
e = (None, None)
ey = None

for line in sys.stdin:
    print(repr(line))
    grid.append([])
    for c in line.strip():
        if c == 'S':
            c = 'a'
            s = (len(grid) - 1, len(grid[-1]))
        elif c == 'E':
            c = 'z'
            e = (len(grid) - 1, len(grid[-1]))
        grid[-1].append(c)
grid = np.array(grid)

print(f"S: {s}")
print(f"E: {e}")
print(grid)

# search


@total_ordering
class Place:
    def __init__(self, x, y, dist):
        self.x = x
        self.y = y
        self.dist = dist

    def __str__(self):
        return f"{self.x}x{self.y}:{self.dist}"

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(self.__str__())

    def __eq__(self, other):
        global grid
        eq_val = self.value() == other.value()
        eq_dist = self.dist == other.dist
        return eq_val and eq_dist

    def __lt__(self, other):
        global grid
        # Prefer shorted path
        if self.dist != other.dist:
            return self.dist < other.dist
        # Prefer tallest path
        return ord(self.value()) > ord(other.value())

    # Value of this place in the grid.
    def value(self):
        global grid
        return grid[self.x][self.y]

    def point(self):
        return (self.x, self.y)

    def coincident(self, other):
        if other is None:
            return False
        return self.point() == other.point()


class Explorer:
    def __init__(self, start, end):
        self.start = Place(start[0], start[1], 0)
        self.end = Place(end[0], end[1], float('inf'))
        # Search state
        self.seen = set([])  # points
        self.paths = []  # places
        # Initialise
        self.add(None, self.start)

    # Add a place to the list of possibles if it is not yet seen.
    def add(self, p, new):
        if new.point() in self.seen:
            return
        if p is not None:
            diff = ord(new.value()) - ord(p.value())
            if diff > 1:
                return
        heapq.heappush(self.paths, new)
        self.seen.add(new.point())

    # return possible next steps for a given place, where possible means a
    # non-visited square not more than one above the current.
    def possibles(self, p):
        global grid
        # up
        if p.x > 0:
            self.add(p, Place(p.x-1, p.y, p.dist+1))
        # down
        if p.x < grid.shape[0]-1:
            self.add(p, Place(p.x+1, p.y, p.dist+1))
        # left
        if p.y > 0:
            self.add(p, Place(p.x, p.y-1, p.dist+1))
        # right
        if p.y < grid.shape[1]-1:
            self.add(p, Place(p.x, p.y+1, p.dist+1))

    def explore(self):
        p = None
        while not self.end.coincident(p):
            p = heapq.heappop(self.paths)
            self.possibles(p)
            print('current paths:', self.paths)
        return p


e = Explorer(s, e)
p = e.explore()
print('final path:', p)
