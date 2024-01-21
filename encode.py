"""Encode a string to 3-bit ternary using a given mapping

The mapping takes the form of an alphabet string such that the first character is encoded to 001
the second character is encoded to 002, etc.

Only encodes alphabet characters (normalised to lowercase).
Any other character is converted to white space and de-duplicated.
"""
import json
import random
import sys
from argparse import ArgumentParser, FileType
from itertools import chain
from string import ascii_lowercase

# pre-calculate a ternary lookup table
TERNARY = [str(i) + str(j) + str(k) for i in range(3) for j in range(3) for k in range(3)]


def main():
    parser = ArgumentParser()
    parser.add_argument("text", type=FileType("r"), help="Input text file, or - to read from stdin")
    parser.add_argument(
        "-o", "--output", type=FileType("w"), default=sys.stdout, help="Output file or stdout by default"
    )
    parser.add_argument("-m", "--mapping", default=ascii_lowercase, help="Mapping alphabet string")
    parser.add_argument("-s", "--separator", default="", help="Separator to use between ternary triples, default none")
    parser.add_argument(
        "-x",
        "--no-spaces",
        dest="spaces",
        action="store_false",
        help="Don't include white space characters (000) in the encoded output",
    )

    args = parser.parse_args()

    assert set(args.mapping) == set(ascii_lowercase), "Incomplete mapping"

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
