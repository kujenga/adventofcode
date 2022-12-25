#!/usr/bin/env python3

import sys
import os


COUNT = int(os.environ.get('KNOTCOUNT', 2))


# vertical, horizonal tuples
rope = [(0, 0)] * COUNT
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
    result = (t[0] + udm, t[1] + lrm)
    return result


# no movement
assert follow((0, 0), (0, 0)) == (0, 0)
assert follow((0, 1), (0, 0)) == (0, 0)
# horizontal movement
assert follow((1, 3), (1, 1)) == (1, 2)
# diagonal movement
assert follow((2, 3), (1, 1)) == (2, 2)


def move(direction):
    global rope
    H = rope[0]
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
    rope[0] = H
    for i, _ in enumerate(rope):
        if i == 0:
            # head is dealt with above
            continue
        v = follow(rope[i-1], rope[i])
        rope[i] = v
        if i == len(rope)-1:
            visited.append(v)


for line in sys.stdin:
    direction, distance = line.strip().split()
    #  print(f"{direction} {distance}")
    for _ in range(0, int(distance)):
        move(direction)
        #  print(rope)

print('visited count:', len(set(visited)))
