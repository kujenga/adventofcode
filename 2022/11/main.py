#!/usr/bin/env python3

import sys
import os
from pprint import pprint


DIVISOR = int(os.environ.get('DIVISOR', '3'))
ROUNDS = int(os.environ.get('ROUNDS', '20'))


class Item:
    def __init__(self, worry, monkeys):
        self.worry = worry
        self.monkeys = monkeys
        pass

    def __str__(self):
        return f"<Item worry={self.worry}, monkeys={len(self.monkeys)}>"

    def inspect(self, monkey):
        worrya = self.worry
        worryb = monkey.op(worrya)
        worryc = worryb // DIVISOR
        test = worryc % monkey.test_divisor == 0
        #  print(f"inspect: {item} -> {worrya} -> {worryb} -> {worryc} -> {test}")
        self.worry = worryc
        return test


class Monkey:
    def __init__(self, name, items=[]):
        self.name = name
        self.op = None
        self.test_divisor = None
        self.if_true = None
        self.if_false = None
        # State
        self.items = items
        self.inspect_count = 0

    def __str__(self):
        return f"<Monkey name={repr(self.name)}, items={len(self.items)}, op={repr(self.op)}, test=/{self.test_divisor}, if_true={repr(self.if_true)}, if_false={repr(self.if_false)}>"  # noqa

    def __repr__(self):
        return self.__str__()

    def inspect(self):
        self.inspect_count += 1
        item = self.items.pop(0)
        return (item, item.inspect(self))


def make_op(operation, operand):
    def op(worry):
        a = worry
        if operand == 'old':
            b = worry
        else:
            b = int(operand)
        if operation == '+':
            return a + b
        elif operation == '*':
            return a * b
        else:
            assert False, f"unknown operation: {operation}"
    return op


monkeys = []
monkey_map = {}

for line in sys.stdin:
    if line.startswith('Monkey '):
        name = int(line[6:].strip(' :\n'))
        m = Monkey(name)
        monkeys.append(m)
        monkey_map[name] = m
    elif line.startswith('  Starting items:'):
        worries = [int(i.strip()) for i in line[17:].split(',')]
        monkeys[-1].items = [Item(w, monkeys) for w in worries]
    elif line.startswith('  Operation:'):
        a, op, b = [o.strip() for o in line[19:].split()]
        assert a == 'old'
        monkeys[-1].op = make_op(op, b)
    elif line.startswith('  Test:'):
        assert 'Test: divisible by' in line
        divisor = int(line[len('  Test: divisible by '):].strip())
        monkeys[-1].test_divisor = divisor
    elif line.startswith('    If true: throw to monkey '):
        start = len('    If true: throw to monkey ')
        monkeys[-1].if_true = int(line[start:].strip())
    elif line.startswith('    If false: throw to monkey '):
        start = len('    If false: throw to monkey ')
        monkeys[-1].if_false = int(line[start:].strip())

print("initial monkeys:")
pprint(monkeys)

for round in range(ROUNDS):
    for monkey in monkeys:
        while len(monkey.items) > 0:
            item, test = monkey.inspect()
            if test:
                monkey_map[monkey.if_true].items.append(item)
            else:
                monkey_map[monkey.if_false].items.append(item)
    print('after round:', round)
    pprint(monkeys)

print("final monkeys:")
pprint(monkeys)

for monkey in monkeys:
    print(f"monkey {monkey.name} inspected {monkey.inspect_count}")

inspect_counts = [m.inspect_count for m in monkeys]
inspect_counts.sort()
print("monkey business:", inspect_counts[-1] * inspect_counts[-2])
