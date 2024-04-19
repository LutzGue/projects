import itertools
import time
from typing import List
import sys
sys.setrecursionlimit(100000)

def generate_combinations(elements: List[str], n: int) -> List[str]:
    return [''.join(p) for p in itertools.product(elements, repeat=n)]

def add_brackets(s: str, h_limit: int, f_limit: int, e_limit: int, h=0, f=0, e=0) -> set:
    if h >= h_limit or f >= f_limit or e >= e_limit or len(s) <= 2:
        return {s}
    else:
        results = set()
        for i in range(1, min(e_limit, len(s) - 1) + 1):
            for j in range(len(s) - i):
                if s[j:j+i+1].strip():
                    t = s[:j] + '(' + s[j:j+i+1] + ')' + s[j+i+1:]
                    if '()' not in t:
                        results.add(t)
                        results.update(add_brackets(t, h_limit, f_limit, e_limit, h+1, f+1, e+1))
        return results

def generate_strings(x: List[str], n: int, h_limit: int, f_limit: int, e_limit: int) -> None:
    combinations = generate_combinations(x, n)
    all_strings = set()
    for combination in combinations:
        all_strings.update(add_brackets(combination, h_limit, f_limit, e_limit))
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    with open(f'output_{timestamp}.txt', 'w') as f:
        for string in all_strings:
            f.write(string + '\n')
    print(f"Anzahl der erzeugten Datensätze: {len(all_strings)}")

# Parameter
x = ["T", "S", "D"]
n = 5
h_limit = 1
f_limit = 1
e_limit = 2

# Ausführung
generate_strings(x, n, h_limit, f_limit, e_limit)
