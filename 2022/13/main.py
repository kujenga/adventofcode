#!/usr/bin/env python3

import sys
import json
import itertools


def ordered(left, right):
    #  print("ordered:", left, right)
    for (l, r) in itertools.zip_longest(left, right):
        #  print("l, r", l, r, type(l), type(r))
        if l is None:
            return True
        if r is None:
            return False
        if type(l) == int and type(r) == int:
            if l < r:
                return True
            if l > r:
                return False
            continue
        elif type(l) == list and type(r) == list:
            o = ordered(l, r)
        elif type(l) == list:
            o = ordered(l, [r])
        elif type(r) == list:
            o = ordered([l], r)
        # Handle true ordering, ignore None.
        if o is True or o is False:
            return o

    return None


index = 1
result = 0
prev = None

for line in sys.stdin:
    line = line.strip()
    # Reset for the next pair on blank lines.
    if line == '':
        index += 1
        prev = None
        continue

    data = json.loads(line)
    # When prev is none, this is the first line in a pair.
    if prev is None:
        prev = data
        continue

    # Check ordering
    o = ordered(prev, data)
    print(f"{index} is ordered: {o}: {prev} <-> {data}")
    if o:
        result += index

print('sum of ordered indexes:', result)
