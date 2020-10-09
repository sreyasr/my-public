import Player2
import argparse
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
# fh = logging.FileHandler("p2.log")
# fh.setLevel(logging.DEBUG)
# logger.addHandler(fh)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str, help="Input File")
    args = parser.parse_args()
    positions = None
    colors = None
    with open(args.input_file, "r") as f:
        lines = f.readlines()
        positions = int(lines[0])
        colors = lines[1].split()

    dic = dict()

    for i in range(len(colors)):
        dic[colors[i]] = i

    player = Player2.player(positions, len(colors))

    X = next(player)

    while True:
        print(*list(map(lambda x: colors[x], X)), sep=" ")

        inp = None

        while inp is None:
            try:
                inp = input()
            except EOFError:
                pass

        if inp.upper() == "YES":
            return
        logger.info("inp: %r" % inp)
        correct_pos, correct_num = list(map(int, inp.strip().split()))
        g = (correct_pos, correct_num)
        logger.info("g: %r, %r" % (correct_pos, correct_num))
        X = player.send(g)


if __name__ == "__main__":
    main()
