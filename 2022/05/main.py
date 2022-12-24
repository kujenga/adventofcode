#!/usr/bin/env python3

import sys
import os
import re
from pprint import pprint


MOVER = os.environ.get('CRATEMOVER', '9000')


stack_re = re.compile(r"(?:(\[[A-Z]+\]|   )(?: |\n))+")
label_re = re.compile(r"(?:( [0-9]+ |   ) ?)+")
move_re = re.compile(r"move ([0-9]+) from ([0-9]+) to ([0-9]+)")


parsing = True
stacks = []

for line in sys.stdin:
    # Parse stack specifiers
    stack = stack_re.match(line)
    if stack is not None:
        assert parsing
        i = 0
        while line != "":
            tok, line = line[:4], line[4:]
            crate = tok.strip('[] \n')
            if len(stacks) <= i:
                stacks.append([])
            if crate != '':
                stacks[i].append(crate)
            i += 1

        continue

    # End parsing when labels seen, reverse parsed stacks.
    label = label_re.match(line)
    if label is not None:
        assert parsing
        parsing = False
        # reverse the stacks so that they look like actual stacks
        for s in stacks:
            s.reverse()
        print('initial stacks:')
        pprint(stacks)
        continue

    # Perform moves.
    move = move_re.match(line)
    if move is not None:
        cnt, frm, to = [int(s) for s in move.groups()]
        if MOVER == '9000':
            for _ in range(0, cnt):
                transfer = stacks[frm-1].pop()
                stacks[to-1].append(transfer)
        elif MOVER == '9001':
            transfer = stacks[frm-1][-cnt:]
            stacks[frm-1] = stacks[frm-1][:-cnt]
            stacks[to-1].extend(transfer)
        continue

    # all other lines must be just empty newlines.
    assert line == "\n", f"line: {repr(line)}"

print('final stacks:')
pprint(stacks)

tops = ""
for stack in stacks:
    tops += stack[-1]
print('top of stacks:', tops)
