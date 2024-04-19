"""
from itertools import product
import datetime

def generate_combinations(x, n):
    return list(product(x, repeat=n))

def write_to_file(result):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"result_{timestamp}.txt", "w") as f:
        for r in result:
            f.write(''.join(r) + "\n")

print(f'count: {len(result)}')

write_to_file(result)

print('DONE')

import sys
sys.setrecursionlimit(10000)

-----------------

def parse_tree_generator(n, start, extend):
    for _ in range(n):
        start = start.replace('<v>', extend, 1)
        start = start.replace('<h>', extend, 1)

    start = start.replace('<v>', '')
    start = start.replace('<h>', '')
    return start

n = 10
start = '["C"_"major"<v>]'

extend ='["<r>"<h>"?"]<v>'

result = parse_tree_generator(n, start, extend)
print(result)


"""