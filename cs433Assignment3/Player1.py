import subprocess
import os
import logging
import random

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("out.txt", mode="w")
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)
error = 0.4


def binomial(p):
    return random.uniform(0, 1) < p


input_file = "input.txt"
RR = [
    "green",
    "blue",
    "yellow",
    "blue",
    "green",
    "red",
    "white",
    "yellow",
    "white",
    "white",
]


def get_correct_pos(li):
    count = 0
    for i in range(len(RR)):
        if RR[i] == li[i]:
            count += 1
    return count


def get_correct_num(li):
    s = set(li)
    count = 0
    for i in s:
        count += min(li.count(i), RR.count(i))
    return count


def main():
    proc = subprocess.Popen(
        ["python3", "p2.py", input_file], stdin=subprocess.PIPE, stdout=subprocess.PIPE
    )
    while True:
        recv = ""
        while recv == "" or recv[-1] != "\n":
            out = os.read(proc.stdout.fileno(), 4096).decode()
            recv += out
        recv = recv[:-1]
        logger.info("P2: %s" % recv)
        li = recv.split()
        correct_pos = get_correct_pos(li)
        correct_num = get_correct_num(li)
        if correct_pos == len(RR):
            logger.info("P1: YES")
            os.write(proc.stdin.fileno(), b"YES")
            return

        if binomial(error):
            correct_num = random.randint(0, len(RR))
            correct_pos = random.randint(0, correct_num)
            xtr = "%s %s\n" % (correct_pos, correct_num)
            logger.info("P1: %s  [INCORRECT]" % xtr[:-1])
        else:
            xtr = "%s %s\n" % (correct_pos, correct_num)
            logger.info("P1: %s" % xtr[:-1])

        os.write(proc.stdin.fileno(), xtr.encode())


if __name__ == "__main__":
    main()