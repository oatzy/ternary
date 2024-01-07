import json
import random
from argparse import ArgumentParser, FileType
from collections import Counter
from itertools import product
from math import log
from string import ascii_lowercase

TERNARY = [str(i) + str(j) + str(k) for i in range(3) for j in range(3) for k in range(3)]


def entropy(p, base=3):
    return -p * log(p, base)


def score_balance(bits):
    c = Counter(bits)
    total = sum(c.values())
    return sum(b and entropy(b / total) for b in c.values())


def score_spread(bits):
    return sum(i != j for i, j in zip(bits, bits[1:])) / (len(bits) - 1)


BIT_SCORES = {
    (i, j): score_balance(TERNARY[i] + TERNARY[j]) * score_spread(TERNARY[i] + TERNARY[j])
    for i, j in product(range(27), range(27))
}


def calculate_score(arrangement, frequencies):
    total = 0
    for pair in product(enumerate(arrangement), enumerate(arrangement)):
        chars = pair[0][1] + pair[1][1]
        total += frequencies.get(chars, 0) * BIT_SCORES[(pair[0][0], pair[1][0])]
    return total


def generate_mapping(frequencies):
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
    parser.add_argument("frequencies", type=FileType("r"))
    parser.add_argument("-n", "--iterations", type=int, default=100)
    parser.add_argument("-p", "--pretty", action="store_true")
    parser.add_argument("--score", help="return the score of an existing mapping")

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
