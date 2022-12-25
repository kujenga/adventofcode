#!/usr/bin/env python3

import sys
from pprint import pprint
from enum import Enum


class Cmd(Enum):
    NOOP = 'noop'
    ADDX = 'addx'

    def cycles(self):
        if self == Cmd.NOOP:
            return 1
        if self == Cmd.ADDX:
            return 2


class CRT:
    def __init__(self):
        # CRT display
        self.display = [['_'] * 40 for _ in range(6)]

    def output(self):
        for row in self.display:
            print(''.join(row))


class VM:
    def __init__(self, program):
        # VM state
        self.program = program
        self.cycles = 0
        # Program execution state
        self.cmd = None
        self.counter = 0
        self.X = 1
        # Signals
        self.signal_strength = []
        # CRT
        self.crt = CRT()

    def __str__(self):
        return f"<cycles({self.cycles}), program({len(program)}), cmd({self.cmd}), ctr({self.counter}), X({self.X})>"

    def cycle(self):
        # update CRT display
        col = self.cycles % 40
        row = int(self.cycles / 40) % 6
        draw = abs((self.cycles % 40) - self.X) <= 1
        #  print(f"{self.cycles}: setting {row}x{col}, sprint center: {self.X}, draw: {draw}")
        if draw:
            self.crt.display[row][col] = '#'
        else:
            self.crt.display[row][col] = '.'

        self.cycles += 1
        #  print(self)
        # capture signal strength
        if (self.cycles - 20) % 40 == 0:
            signal = self.X * self.cycles
            print(f"capturing at {self.cycles} signal {signal}")
            self.signal_strength.append(signal)


    def step(self):
        # Then execute the effects of that command on the VM.
        if self.counter == 0:
            # start new cycle
            self.cmd = self.program.pop()
            self.counter = self.cmd[0].cycles()
        if self.counter > 0:
            self.counter -= 1

        # Clock cycle first
        self.cycle()

        # Then execute when in zero counter state (execution complete)
        if self.counter == 0:
            if self.cmd[0] == Cmd.ADDX:
                self.X += self.cmd[1]

    def run(self):
        while len(self.program) > 0 or self.counter > 0:
            self.step()
            #  vm.crt.output()


program = []
for line in sys.stdin:
    args = line.strip().split()
    command = args[0]
    if command == 'noop':
        program.append((Cmd(command), None))
    elif command == 'addx':
        program.append((Cmd(command), int(args[1])))
    else:
        assert False, f"unknown command: {command}"
program.reverse()

pprint(program)

vm = VM(program)
vm.run()

print('cycles:', vm.cycles)

print('signal strengths:', vm.signal_strength)
print('signal strength sum:', sum(vm.signal_strength))

print('CRT:')
vm.crt.output()
