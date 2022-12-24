#!/usr/bin/env python3

import sys


# vertical, horizonal tuples
H = (0, 0)
T = (0, 0)
visited = []


def move_dist(n, diag=False):
    if n == 0:
        return 0
    if abs(n) == 1:
        # When diagonal, we are always moving.
        if not diag:
            return 0
    if n > 0:
        return 1
    if n < 0:
        return -1
    assert False


def follow(h, t):
    ud = (h[0] - t[0])
    lr = (h[1] - t[1])
    udm = 0
    lrm = 0
    if ud == lr == 0:
        pass
    elif ud == 0:
        lrm = move_dist(lr)
    elif lr == 0:
        udm = move_dist(ud)
    elif abs(ud) > 1 or abs(lr) > 1:
        lrm = move_dist(lr, diag=True)
        udm = move_dist(ud, diag=True)
    return (t[0] + udm, t[1] + lrm)


# no movement
assert follow((0, 0), (0, 0)) == (0, 0)
assert follow((0, 1), (0, 0)) == (0, 0)
# horizontal movement
assert follow((1, 3), (1, 1)) == (1, 2)
# diagonal movement
assert follow((2, 3), (1, 1)) == (2, 2)


def move(direction):
    global H
    global T
    if direction == 'R':
        H = (H[0], H[1]+1)
        pass
    elif direction == 'L':
        H = (H[0], H[1]-1)
        pass
    elif direction == 'U':
        H = (H[0]+1, H[1])
        pass
    elif direction == 'D':
        H = (H[0]-1, H[1])
        pass
    T = follow(H, T)
    visited.append(T)



for line in sys.stdin:
    direction, distance = line.strip().split()
    for _ in range(0, int(distance)):
        move(direction)

print('visited count:', len(set(visited)))
