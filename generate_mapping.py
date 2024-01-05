import json
import random
from argparse import ArgumentParser, FileType
from collections import Counter
from itertools import product
from functools import lru_cache
from math import log
from string import ascii_lowercase

TERNARY = [str(i)+str(j)+str(k) for i in range(3) for j in range(3) for k in range(3)]

def entropy(p, base=3):
    return -p * log(p, base)

def score_balance(bits):
    c = Counter(bits)
    total = sum(c.values())
    return sum(b and entropy(b/total) for b in c.values())

def score_spread(bits):
    return sum(i!=j for i,j in zip(bits, bits[1:]))/(len(bits)-1)

BIT_SCORES = {
    (i,j): score_balance(TERNARY[i] + TERNARY[j]) * score_spread(TERNARY[i] + TERNARY[j])
    for i,j in product(range(27), range(27))
}

def calculate_score(arrangement, frequencies):
    total = 0
    for pair in product(enumerate(arrangement), enumerate(arrangement)):
        chars = pair[0][1] + pair[1][1]
        total += frequencies.get(chars, 0) * BIT_SCORES[(pair[0][0], pair[1][0])]
    return total


def should_keep(t):
    return t < 10  # random.random() > 0.9


def main():
    parser = ArgumentParser()
    parser.add_argument("frequencies", type=FileType("r"))
    parser.add_argument("-i", "--initial", default=ascii_lowercase)
    parser.add_argument("-n", "--iterations", type=int, default=10_000)
    parser.add_argument("-p", "--pretty", action="store_true")

    args = parser.parse_args()

    frequencies = json.load(args.frequencies)
    arr = [" "] + [c for c in args.initial if c in ascii_lowercase]
    assert len(arr) == 27, "Missing characters"

    score = calculate_score(arr, frequencies)
    swaps = 0
    for t in range(args.iterations):

        i = random.randint(1, 26)
        j = random.randint(1, 26)
        if i == j:
            j = max(1, 17 * j % 26) 

        arr[i], arr[j] = arr[j], arr[i]

        new_score = calculate_score(arr, frequencies)

        if new_score >= score or should_keep(t):
            score = new_score
            swaps += 1
        else:
            arr[i], arr[j] = arr[j], arr[i]

    score /= sum(frequencies.values())

    if not args.pretty:
        print(f'{"".join(arr[1:])}:{score}')
        return

    print("Score:", score)
    print("Swaps:", swaps)
    print("Mapping:\n")

    for c, i in sorted(((c, i) for i, c in enumerate(arr))):
        print(f'{c} -> {"".join(str(b) for b in TERNARY[i])}')



if __name__ == '__main__':
    main()
