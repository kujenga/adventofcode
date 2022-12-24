#!/usr/bin/env python3

import sys


def parse_range(r):
    start, end = [int(i) for i in r.strip().split('-')]
    return range(start, end)


def parse_row(r):
    a, b = [parse_range(x) for x in r.strip().split(',')]
    return (a, b)


assert parse_row('1-2,3-4') == (range(1, 2), range(3, 4))


def contains(a, b):
    if a.start >= b.start and a.stop <= b.stop:
        return True
    if b.start >= a.start and b.stop <= a.stop:
        return True
    return False


def overlap(a, b):
    if a.start >= b.start and a.start <= b.stop:
        return True
    if a.stop >= b.start and a.stop <= b.stop:
        return True
    if b.start >= a.start and b.start <= a.stop:
        return True
    if b.stop >= a.start and b.stop <= a.stop:
        return True
    return False


total_contains = 0
total_overlap = 0

for line in sys.stdin:
    a, b = parse_row(line)
    if contains(a, b):
        total_contains += 1
    if overlap(a, b):
        total_overlap += 1

print('total contains:', total_contains)
print('total overlap:', total_overlap)
