#!/usr/bin/env python3

import sys
import re
import os

sensor_re = re.compile(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")  # noqa


def manhattan_dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


# Basic validations for manhattan_dist function.
assert manhattan_dist((0, 0), (4, 4)) == 8
assert manhattan_dist((-1, -4), (2, 2)) == 9


class Finding:
    def __init__(self, sx, sy, bx, by):
        self.s = (sx, sy)
        self.b = (bx, by)

    def __str__(self):
        return f"<Finding sensor{self.s} beacon{self.b} dist={self.manhattan_dist()}>"  # noqa

    def manhattan_dist(self):
        return manhattan_dist(self.s, self.b)

    def confirmed_empty(self, p):
        if self.manhattan_dist() >= manhattan_dist(self.s, p):
            return True


findings = []
for line in sys.stdin:
    m = sensor_re.match(line.strip())
    assert m is not None, f"no match for line: {repr(line)}"

    sx, sy, bx, by = [int(v) for v in m.groups()]
    findings.append(Finding(sx, sy, bx, by))

LINE = int(os.environ.get('LINE_NUM', '10'))

# Identify grid boundaries
minx = 0
maxx = 0
for f in findings:
    print(f)
    d = f.manhattan_dist()
    pminx = f.s[0] - d
    if pminx < minx:
        minx = pminx
    pmaxx = f.s[0] + d
    if pmaxx > maxx:
        maxx = pmaxx

print(f"range({minx}, {maxx})")

unfound = 0
for i in range(minx, maxx):
    p = (i, LINE)
    if i % 100000 == 0:
        print(p)
    # For each finding, break if this is a beacon:
    beacon = False
    for f in findings:
        if p == f.b:
            beacon = True
    if beacon:
        continue
    # For each finding, see if this is confirmed empty.
    for f in findings:
        if f.confirmed_empty(p):
            #  print(f"point confirmed empty: {p} for {f}")
            unfound += 1
            break

print('Unfound:', unfound)
