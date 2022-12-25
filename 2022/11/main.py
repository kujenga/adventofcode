#!/usr/bin/env python3

import sys
from pprint import pprint


class Monkey:
    def __init__(self, name, items=[]):
        self.name = name
        self.op = None
        self.test = None
        self.if_true = None
        self.if_false = None
        # State
        self.items = items
        self.inspect_count = 0

    def __str__(self):
        return f"<Monkey name={repr(self.name)}, items={repr(self.items)}, op={repr(self.op)}, test={repr(self.test)}, if_true={repr(self.if_true)}, if_false={repr(self.if_false)}>"  # noqa

    def __repr__(self):
        return self.__str__()

    def inspect(self):
        self.inspect_count += 1
        item = self.items.pop(0)
        worrya = item
        worryb = self.op(worrya)
        worryc = int(worryb / 3)
        test = self.test(worryc)
        #  print(f"inspect: {item} -> {worrya} -> {worryb} -> {worryc} -> {test}")
        return (worryc, test)


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


def make_test(divisor):
    def test(worry):
        return worry % divisor == 0
    return test


monkeys = []
monkey_map = {}

for line in sys.stdin:
    if line.startswith('Monkey '):
        name = int(line[6:].strip(' :\n'))
        m = Monkey(name)
        monkeys.append(m)
        monkey_map[name] = m
    elif line.startswith('  Starting items:'):
        monkeys[-1].items = [int(i.strip()) for i in line[17:].split(',')]
    elif line.startswith('  Operation:'):
        a, op, b = [o.strip() for o in line[19:].split()]
        assert a == 'old'
        monkeys[-1].op = make_op(op, b)
    elif line.startswith('  Test:'):
        assert 'Test: divisible by' in line
        divisor = int(line[len('  Test: divisible by '):].strip())
        monkeys[-1].test = make_test(divisor)
    elif line.startswith('    If true: throw to monkey '):
        start = len('    If true: throw to monkey ')
        monkeys[-1].if_true = int(line[start:].strip())
    elif line.startswith('    If false: throw to monkey '):
        start = len('    If false: throw to monkey ')
        monkeys[-1].if_false = int(line[start:].strip())

print("initial monkeys:")
pprint(monkeys)

rounds = 20

for round in range(rounds):
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
