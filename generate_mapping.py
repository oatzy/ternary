"""Try to generate an optimal mapping of letters to 3-bit ternary

Based on input 2-gram frequencies.
"""
import json
import random
from argparse import ArgumentParser, FileType
from collections import Counter
from itertools import product
from math import log
from string import ascii_lowercase

# pre-calculate ternary lookup table
TERNARY = [str(i) + str(j) + str(k) for i in range(3) for j in range(3) for k in range(3)]


def entropy(p, base=3):
    """Calculate entropy of a probability 'p' in base 3 by default"""
    return -p * log(p, base)


def score_balance(bits):
    """Calculate the 'balance' of bits in a string.

    Balance is the total entropy for all bit types in the string
    """
    c = Counter(bits)
    total = sum(c.values())
    return sum(b and entropy(b / total) for b in c.values())


def score_spread(bits):
    """Calculate how spread out bits are in a string.

    That is, repeated bits increase the score
    """
    return sum(i != j for i, j in zip(bits, bits[1:])) / (len(bits) - 1)


# pre-calculate the pair score look up table
# there are 27*27=729 pairs of codes and we need to refer to them often during optimisation
# so it's much more effecient to pre-calculate them
BIT_SCORES = {
    (i, j): score_balance(TERNARY[i] + TERNARY[j]) * score_spread(TERNARY[i] + TERNARY[j])
    for i, j in product(range(27), range(27))
}


def calculate_score(arrangement, frequencies):
    """Calculate the score for a given mapping of characters to ternary triples.

    For each given pair of characters, we multiple its frequency by the score
    of the encoding assigned to it, then take the sum across all possible pairs.
    """
    total = 0
    for pair in product(enumerate(arrangement), enumerate(arrangement)):
        chars = pair[0][1] + pair[1][1]
        total += frequencies.get(chars, 0) * BIT_SCORES[(pair[0][0], pair[1][0])]
    return total


def generate_mapping(frequencies):
    """Generate a possible optimal mapping.

    Starts with a random mapping, then tries to increase its score
    by swapping pairs of character encodings
    """
    # white space is pinned as 000
    arr = [" "] + random.sample(ascii_lowercase, 26)

    score = calculate_score(arr, frequencies)
    while True:
        old_score = score
        for i in range(1, 27):
            best = i
            for j in range(i + 1, 27):
                arr[i], arr[j] = arr[j], arr[i]

                new_score = calculate_score(arr, frequencies)

                if new_score >= score:
                    score = new_score
                    best = j

                arr[i], arr[j] = arr[j], arr[i]

            arr[i], arr[best] = arr[best], arr[i]

        if score == old_score:
            break

    return arr, score


def main():
    parser = ArgumentParser()
    parser.add_argument("frequencies", type=FileType("r"), help="Json-formated file containing letter pair frequencies")
    parser.add_argument(
        "-n", "--iterations", type=int, default=100, help="number of potential mappings to generate and compare"
    )
    parser.add_argument(
        "-p", "--pretty", action="store_true", help="pretty-print the generated mapping, default compact format"
    )
    parser.add_argument("--score", help="return the score of an existing mapping; don't generate a new one")

    args = parser.parse_args()

    frequencies = json.load(args.frequencies)

    if args.score:
        arr = [" "] + list(args.score)
        score = calculate_score(arr, frequencies)

    else:
        score = 0
        arr = []
        for _ in range(args.iterations):
            new_arr, new_score = generate_mapping(frequencies)
            if new_score > score:
                score = new_score
                arr = new_arr

    # normalise the score to [0,1]
    score /= sum(frequencies.values())

    if not args.pretty:
        print(f'{"".join(arr[1:])}:{score}')
        return

    print("Score:", score)
    print("Mapping:\n")

    for c, i in sorted(((c, i) for i, c in enumerate(arr))):
        print(f'{c} -> {"".join(str(b) for b in TERNARY[i])}')


if __name__ == "__main__":
    main()
