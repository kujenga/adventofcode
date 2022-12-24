#!/usr/bin/env python3

import sys
from pathlib import Path

# interpret directory structure.

mode = ''
workdir = Path('')


class Entry:
    def __init__(self, name, size=None):
        self.name = name
        self.size = size  # None for dirs
        if self.size is None:
            self.sub = {}

    def __str__(self):
        if self.size is not None:
            return f"{self.name}: {self.size}"
        return f"{self.name}: <dir>"

    def print(self, indent=''):
        if self.size is not None:
            print(f"{indent}{self}")
            return
        print(f"{indent}{self}")
        for k in self.sub:
            self.sub[k].print(indent+'  ')


# Root filesystem
files = Entry('elves://')


def add(path, e):
    global files
    target = files.sub
    # Find the target
    for p in path.parts:
        if p not in target:
            target[p] = Entry(p)
        target = target[p].sub
    target[e.name] = e


for line in sys.stdin:
    if line.startswith('$'):
        args = line.split()[1:]
        if args[0] == 'cd':
            workdir = Path(workdir, args[1]).resolve()
        if args[0] == 'ls':
            mode = 'ls'
        else:
            mode = ''
        # command
    elif mode == 'ls':
        info, name = line.split()
        if info == 'dir':
            add(workdir, Entry(name))
        else:
            add(workdir, Entry(name, int(info)))

print('file structure:')
files.print()

# calculate directory sizes


sizes = []


def calc_size(entry):
    global sizes
    size = 0
    for k in entry.sub:
        v = entry.sub[k]
        if v.size is None:
            size += calc_size(v)
        else:
            size += v.size
    sizes.append(size)
    return size

print('calculated sizes:', calc_size(files))
print('sizes:', sizes)

result = sum(filter(lambda v: v < 100_000, sizes))
print('result:', result)
