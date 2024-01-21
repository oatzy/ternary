"""Count the number of n-grams (substrings of letters) in an input text

Output is a json dictionary of n-grams to total counts

Only considers alphabetical characters (normalised to lowercase) and white space. 
Any other character is treated as white space (making them effective word boundries)
and repeated white space characters are de-duplicated.
"""
import json
import sys

from argparse import ArgumentParser, FileType
from collections import Counter, deque
from itertools import chain
from string import ascii_lowercase


ALLOW_CHARS = ascii_lowercase


def count_ngrams(chars, n=2):
    counts = Counter()

    cur = deque([" "], n)
    for c in chars:
        c = c.lower()

        if c not in ALLOW_CHARS:
            if cur[-1] == " ":
                continue
            c = " "

        cur.append(c)

        if len(cur) < n:
            continue

        counts.update(["".join(cur)])

    return counts


def main():
    parser = ArgumentParser()
    parser.add_argument("input", type=FileType("r"), help="Input file path or - to read from stdin")
    parser.add_argument("-n", default=2, type=int, help="size of n-gram to count")
    parser.add_argument(
        "-o", "--output", type=FileType("w"), default=sys.stdout, help="Output file or stdout by default"
    )

    args = parser.parse_args()

    chars = chain.from_iterable(args.input)
    counts = count_ngrams(chars, n=args.n)
    json.dump(counts, args.output)


if __name__ == "__main__":
    main()
