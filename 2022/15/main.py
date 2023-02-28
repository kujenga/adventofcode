#!/usr/bin/env python3

import sys
import re
import os
from dataclasses import dataclass

sensor_re = re.compile(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")  # noqa


@dataclass(frozen=True)
class Point:
    x: int
    y: int


def manhattan_dist(p1, p2):
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


# Basic validations for manhattan_dist function.
assert manhattan_dist(Point(0, 0), Point(4, 4)) == 8
assert manhattan_dist(Point(-1, -4), Point(2, 2)) == 9


class Finding:
    def __init__(self, sx, sy, bx, by):
        self.s = Point(sx, sy)
        self.b = Point(bx, by)

    def __str__(self):
        return f"<Finding sensor{self.s} beacon{self.b} dist={self.manhattan_dist()}>"  # noqa

    def manhattan_dist(self):
        """Compute the manhattan/taxicab distance between sensor and beacon."""
        return manhattan_dist(self.s, self.b)

    def confirmed_empty(self, p):
        """Returns True when a given point is confirmed as being empty."""
        if self.manhattan_dist() >= manhattan_dist(self.s, p):
            return True

    def xminmax(self, line):
        """Return the min/max x index that a searcher can jump to given this
        beacon, that has not been searched by it."""
        # Manhattan distance available in the x direction for the line.
        d = self.manhattan_dist()
        ydist = abs(self.s.y - line)
        xdist = d - ydist
        return (self.s.x - xdist, self.s.x + xdist)


findings = []
for line in sys.stdin:
    m = sensor_re.match(line.strip())
    assert m is not None, f"no match for line: {repr(line)}"

    sx, sy, bx, by = [int(v) for v in m.groups()]
    findings.append(Finding(sx, sy, bx, by))

# Identify grid boundarie, unless pre-specified.
minx = os.environ.get('MINX')
maxx = os.environ.get('MAXX')
if minx is None or maxx is None:
    minx = 0
    maxx = 0
    for f in findings:
        print(f)
        d = f.manhattan_dist()
        pminx = f.s.x - d
        if pminx < minx:
            minx = pminx
        pmaxx = f.s.x + d
        if pmaxx > maxx:
            maxx = pmaxx


def iterate(line):
    print(f"range({minx}, {maxx})")
    i = minx
    unfound = 0
    while i < maxx:
        p = (i, line)
        #  print(p)
        if i % 100000 == 0:
            print(p)
        jumped = False
        # For each finding, see if this is confirmed empty.
        for f in findings:
            # If we are in the finding range, we jump ahead and count the spots
            # we move ahead in our total covered spots.
            (jmin, jmax) = f.xminmax(line)
            if jmin <= i and jmax > i + 1:
                jump = jmax - i
                print(f"jumping {jump} from {i} to {jmax} based on {f}")
                unfound += jump
                i += jump
                jumped = True
                break
        if not jumped:
            i += 1
    print(unfound)
    # Subtract the count of beacons in this row.
    beacons = set([f.b for f in findings if f.b.x == line])
    print(f"beacons in line: {beacons}")
    unfound -= len(beacons)
    return unfound


# Part 1
LINE = int(os.environ.get('LINE_NUM', '10'))
unfound = iterate(LINE)
print(f"Unfound for line {LINE}:", unfound)
