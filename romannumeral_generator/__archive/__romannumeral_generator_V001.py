#from itertools import product
import datetime

def generate_combinations(elements, n):
    if n == 0:
        return [[]]
    else:
        combinations = []
        for i in range(len(elements)):
            rest_combinations = generate_combinations(elements[i:], n - 1)
            for combination in rest_combinations:
                combinations.append([elements[i]] + combination)
        return combinations

def add_brackets(combination, h):
    if h == 0 or len(combination) == 1:
        return [combination]
    else:
        bracketed_combinations = []
        for i in range(1, len(combination)):
            prefix = combination[:i]
            suffixes = add_brackets(combination[i:], h - 1)
            for suffix in suffixes:
                bracketed_combinations.append(prefix + ['(' + ';'.join(suffix) + ')'])
        return bracketed_combinations

def harmonize_notes(x, n, h_limit):
    combinations = generate_combinations(x, n)
    all_combinations = []
    for h in range(h_limit + 1):
        for combination in combinations:
            all_combinations.extend(add_brackets(combination, h))
    return all_combinations

def write_to_file(result):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"result_{timestamp}.txt", "w") as f:
        for r in result:
            f.write(''.join(r) + "\n")

# Test the function
x = ["T", "S", "D"]
n = 5
h_limit = 2

result = harmonize_notes(x, n, h_limit)

print(f'count: {len(result)}.')
write_to_file(result)
print('DONE')