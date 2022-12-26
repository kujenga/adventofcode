#!/usr/bin/env python3

import sys
import json
import itertools
from functools import cmp_to_key
from pprint import pprint


def ordered(left, right):
    #  print(f"ordered: left: {left} ; right: {right}", left, right)
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


def cmp(left, right):
    o = ordered(left, right)
    if o is None:
        return 0
    if o is True:
        return -1
    if o is False:
        return 1
    assert False, f"unknown ordering: {o}"


index = 1
result = 0
prev = None
packets = []

for line in sys.stdin:
    line = line.strip()
    # Reset for the next pair on blank lines.
    if line == '':
        index += 1
        prev = None
        continue

    data = json.loads(line)
    packets.append(data)
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

# Order and find dividers

# Add dividers
packets.append([[2]])
packets.append([[6]])

print('ordering packets:')
pprint(packets)

# sort packets
packets.sort(key=cmp_to_key(cmp))

print('ordered packets:')
pprint(packets)

# look for dividers
div1 = None
div2 = None
for (i, pkt) in enumerate(packets):
    if type(pkt) != list:
        continue
    if len(pkt) != 1:
        continue
    if type(pkt[0]) != list:
        continue
    if len(pkt[0]) != 1:
        continue
    if pkt[0][0] == 2:
        div1 = i + 1
    if pkt[0][0] == 6:
        div2 = i + 1

print('divider mul:', div1 * div2)
