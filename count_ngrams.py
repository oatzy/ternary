import json
import sys

from argparse import ArgumentParser, FileType
from collections import Counter
from itertools import chain
from string import ascii_lowercase


ALLOW_CHARS = ascii_lowercase


def count_ngrams(chars, n=2):
    counts = Counter()

    cur = [" "]
    for c in chars:
        c = c.lower()

        if c not in ALLOW_CHARS:
            if cur[-1] == " ":
                continue
            c = " "

        cur.append(c)

        if len(cur) >= n:
            cur = cur[-n:]
            counts.update(["".join(cur)])

    return counts


def main():
    parser = ArgumentParser()
    parser.add_argument("input", type=FileType("r"))
    parser.add_argument("-n", default=2, type=int)
    parser.add_argument("-o", "--output", type=FileType("w"), default=sys.stdout)

    args = parser.parse_args()

    chars = chain.from_iterable(args.input)
    counts = count_ngrams(chars, n=args.n)
    json.dump(counts, args.output)


if __name__ == "__main__":
    main()
