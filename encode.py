import json
import random
import sys
from argparse import ArgumentParser, FileType
from itertools import chain
from string import ascii_lowercase

TERNARY = [str(i) + str(j) + str(k) for i in range(3) for j in range(3) for k in range(3)]


def main():
    parser = ArgumentParser()
    parser.add_argument("text", type=FileType("r"))
    parser.add_argument("-o", "--output", type=FileType("w"), default=sys.stdout)
    parser.add_argument("-m", "--mapping", default=ascii_lowercase)
    parser.add_argument("-s", "--separator", default="")
    parser.add_argument("-x", "--no-spaces", dest="spaces", action="store_false")

    args = parser.parse_args()

    mapping = " " + args.mapping
    end = args.separator

    current = " "
    for c in chain.from_iterable(args.text):
        c = c.lower()

        if c not in ascii_lowercase:
            if current == " ":
                continue
            c = " "

        current = c
        if current == " " and not args.spaces:
            continue

        print(TERNARY[mapping.index(c)], end=end, file=args.output)

    print()


if __name__ == "__main__":
    main()
