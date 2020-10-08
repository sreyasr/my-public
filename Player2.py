#!/usr/bin/python3
from z3 import *
import functools
import argparse
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('Player2.log')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)


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

    C = []
    C.append(And(*(cond0 + cond1 + cond2 + cond3)))

    s = Solver()
    while True:
        N = len(C) - 1
        s.add(C[-1])
        if s.check() == unsat:
            raise NotImplementedError
        else:
            X = []
            for i in range(positions):
                for j in range(colors):
                    if s.model()[p[i][j]].as_long() == 1:
                        X.append(j)
                        break
            inp = (yield X)

            correct_pos, correct_num = inp

            cond1 = [p[i][X[i]] for i in range(positions)]
            cond2 = [beta[val][X.count(val)] for val in list(set(X))]
            cond3 = And(
                functools.reduce(lambda x, y: x + y, cond1) == correct_pos,
                functools.reduce(lambda x, y: x + y, cond2) == correct_num,
            )
            C.append(cond3)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("positions", type=int, help="number of positions")
    parser.add_argument("colors", type=int, help="number of colors")
    args = parser.parse_args()
    player(args.positions, args.colors)


if __name__ == "__main__":
    main()
