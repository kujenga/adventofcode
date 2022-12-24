#!/usr/bin/env python3

import sys


def check_start(line, chars=4):
    for i, c in enumerate(line):
        end = i + chars
        possible = line[i:end]
        check = set(possible)
        if len(check) == chars:
            return end


for line in sys.stdin:
    ps = check_start(line, chars=4)
    ms = check_start(line, chars=14)
    print(f"line: {repr(line)}, packet start: {ps}, message start: {ms}")
