import itertools
import time
from typing import List

def generate_combinations(elements: List[str], n: int) -> List[str]:
    return [''.join(p) for p in itertools.product(elements, repeat=n)]

def add_brackets(s: str, h_limit: int, f_limit: int, e_limit: int, h=0, f=0, e=0) -> set:
    if h >= h_limit or f >= f_limit or e >= e_limit or len(s) <= 2:
        return {s}
    else:
        results = set()
        for i in range(1, min(e_limit, len(s)) + 1):
            for j in range(len(s) - i + 1):
                if s[j:j+i].strip():
                    t = s[:j] + '(' + s[j:j+i] + ')' + s[j+i:]
                    if '()' not in t:
                        results.add(t)
                        results.update(add_brackets(t, h_limit, f_limit, e_limit, h+1, f+1, e+1))
        return results

def is_valid(s: str) -> bool:
    count = 0
    for char in s:
        if char == '(':
            count += 1
        elif char == ')':
            if count == 0:
                return False
            count -= 1
    return count == 0

def remove_outer_brackets(s: str) -> str:
    while s.startswith('(') and s.endswith(')') and is_valid(s[1:-1]):
        s = s[1:-1]
    return s

def check_rule(s: str) -> str:
    for i in range(len(s) - 1):
        if s[i] == ')' and (i == len(s) - 1 or s[i+1] == '('):
            return "***ERR: " + s
    if s.endswith(')'):
        return "***ERR: " + s
    return s

def generate_strings(x: List[str], n: int, h_limit: int, f_limit: int, e_limit: int) -> None:
    combinations = generate_combinations(x, n)
    all_strings = set()
    for combination in combinations:
        all_strings.update(add_brackets(combination, h_limit, f_limit, e_limit))
    all_strings = {check_rule(remove_outer_brackets(s)) for s in all_strings}
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    with open(f'output_{timestamp}.txt', 'w') as f:
        for string in all_strings:
            f.write(string + '\n')
    print(f"Anzahl der erzeugten Datensätze: {len(all_strings)}")

# Parameter
x = ["T", "S", "D"]
n = 5
h_limit = 2
f_limit = h_limit
e_limit = n

# Ausführung
generate_strings(x, n, h_limit, f_limit, e_limit)
