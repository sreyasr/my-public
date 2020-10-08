#!/usr/bin/python3
from z3 import *
import functools
import argparse
import logging
from collections import namedtuple

import random

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("Player2.log")
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)


def binomial(p):
    return random.uniform(0, 1) < p


class ClauseHistory:
    def __init__(self):
        self.hist_clause = []
        self.usage_clause = []

    def __getitem__(self, key):
        return self.usage_clause[key][0]

    def append(self, obj, level):
        self.usage_clause.append([obj, level, 1])

    def __len__(self):
        return len(self.usage_clause)

    def update_confidence(self, *args):
        for i in args:
            self.usage_clause[i][2] /= 2

    def get_confidence(self, i):
        return binomial(self.usage_clause[i][3])

    def pop(self):
        self.hist_clause.append(self.usage_clause.pop())


# Suppose the real positions and colors that we want to find be RR


def min2(a, b):
    return If(a > b, b, a)


def player(positions, colors):
    p = [
        [Int("p_%s_%s" % (i, j)) for i in range(colors)] for j in range(positions)
    ]  # p[a][b] is true if color a is at position b
    beta = [
        [Int("beta_%s_%s" % (i, j)) for i in range(positions + 1)]
        for j in range(colors)
    ]  # beta[a][b] is min(sum_p[a], b)

    cond0 = [functools.reduce(lambda x, y: x + y, i) == 1 for i in p]
    cond1 = [p[i][j] >= 0 for i in range(positions) for j in range(colors)]
    cond2 = [p[i][j] <= 1 for i in range(positions) for j in range(colors)]

    def column_sum(i):
        return [row[i] for row in p]

    sum_p = [
        functools.reduce(lambda x, y: x + y, column_sum(i)) for i in range(colors)
    ]  # alp[a] is the number of colors of a in RR
    cond3 = [
        beta[i][j] == min2(sum_p[i], j)
        for i in range(colors)
        for j in range(positions + 1)
    ]

    C = ClauseHistory()
    level = 0
    C.append(And(*(cond0 + cond1 + cond2 + cond3)), level)

    s = Solver()
    s.set(unsat_core=True)
    s.add(C[-1])

    while True:
        if s.check() == unsat:
            unsat_core = s.unsat_core()
            unsat_core_level = list(
                map(lambda x: int(str(x).split("_")[-1]), unsat_core)
            )
            for i in range(len(C) - min(unsat_core_level)):
                s.pop()
                C.pop()
            min_unsat_core = min(unsat_core_level)
            level = len(C) - 1

            # C.update_confidence(*unsat_core_level)
            # for i in range(min_unsat_core, len(C)):
            #     s.push()
            #     s.assert_and_track(C[i], "C_%s" % i)

            continue
        else:
            X = [
                j
                for i in range(positions)
                for j in range(colors)
                if s.model()[p[i][j]].as_long() == 1
            ]
            inp = yield X

            correct_pos, correct_num = inp

            cond1 = [p[i][X[i]] for i in range(positions)]
            cond2 = [beta[val][X.count(val)] for val in list(set(X))]
            cond3 = And(
                functools.reduce(lambda x, y: x + y, cond1) == correct_pos,
                functools.reduce(lambda x, y: x + y, cond2) == correct_num,
            )
            level += 1
            C.append(cond3, level)
            s.push()
            s.assert_and_track(C[-1], "C_%s" % level)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("positions", type=int, help="number of positions")
    parser.add_argument("colors", type=int, help="number of colors")
    args = parser.parse_args()
    player(args.positions, args.colors)


if __name__ == "__main__":
    main()
