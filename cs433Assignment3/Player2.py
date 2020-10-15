#!/usr/bin/python3
from z3 import *
import functools
import argparse
import logging

import random

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
# fh = logging.FileHandler("Player2.log")
# fh.setLevel(logging.DEBUG)
# logger.addHandler(fh)


def binomial(p):
    return random.uniform(0, 1) < p


class ClauseHistory:
    def __init__(self):
        self.hist_clause = []
        self.usage_clause = []

    def __getitem__(self, key):
        return self.usage_clause[key][0]

    def append(self, obj):
        self.usage_clause.append((obj, 1))

    def __len__(self):
        return len(self.usage_clause)

    def update_confidence(self, *args):
        for i in args:
            m = self.usage_clause[i]
            self.usage_clause[i] = (m[0], m[1]/2)

    def pop(self):
        self.hist_clause.append(self.usage_clause.pop())

    def additional_clauses(self, s, level):
        self.hist_clause.sort(key=lambda x: x[1], reverse=True)
        for i in self.hist_clause.copy():
            if i[1] < 0.20:
                self.hist_clause.remove(i)
                continue
            if binomial(i[1]):
                self.usage_clause.append(i)
                level += 1
                s.push()
                s.assert_and_track(self.usage_clause[-1][0], "C_%s" % level)
                self.hist_clause.remove(i)

        return level


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

    clause_history = ClauseHistory()
    level = 0
    clause_history.append(And(*(cond0 + cond1 + cond2 + cond3)))

    s = Solver()
    s.set(unsat_core=True)
    s.add(clause_history[-1])

    while True:
        if s.check() == unsat:
            unsat_core = s.unsat_core()
            unsat_core_level = list(
                map(lambda x: int(str(x).split("_")[-1]), unsat_core)
            )
            clause_history.update_confidence(*unsat_core_level)
            for i in range(len(clause_history) - min(unsat_core_level)):
                s.pop()
                clause_history.pop()
            level = len(clause_history) - 1
            level = clause_history.additional_clauses(s, level)
            if level != len(clause_history) - 1:
                logger.debug("ValueError: %s %s" % (level, len(clause_history)))
                raise ValueError
            continue
        else:
            guess = [
                j
                for i in range(positions)
                for j in range(colors)
                if s.model()[p[i][j]].as_long() == 1
            ]
            inp = yield guess

            correct_pos, correct_num = inp

            cond1 = [p[i][guess[i]] for i in range(positions)]
            cond2 = [beta[val][guess.count(val)] for val in list(set(guess))]
            cond3 = And(
                functools.reduce(lambda x, y: x + y, cond1) == correct_pos,
                functools.reduce(lambda x, y: x + y, cond2) == correct_num,
            )
            level += 1
            clause_history.append(cond3)
            s.push()
            s.assert_and_track(clause_history[-1], "C_%s" % level)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("positions", type=int, help="number of positions")
    parser.add_argument("colors", type=int, help="number of colors")
    args = parser.parse_args()
    player(args.positions, args.colors)


if __name__ == "__main__":
    main()
