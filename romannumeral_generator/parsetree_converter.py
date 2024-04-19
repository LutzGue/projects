import ast

def find_paths(tree, path=[]):
    if isinstance(tree, list):
        for i, node in enumerate(tree):
            if isinstance(node, list):
                for result in find_paths(node, path + [tree[0]]):
                    yield result
            elif isinstance(node, str) and node.endswith('?'):
                yield path + [tree[0]]

def parse_tree_to_paths(parse_tree):
    tree = ast.literal_eval(parse_tree)
    paths = list(find_paths(tree))
    paths = ['|'.join(reversed(path)) for path in paths]
    return paths

def count_elements_in_paths(paths):
    counts = [path.count('|') for path in paths]  # Add 1 because count('|') will be one less than the number of elements
    return list(zip(paths, counts))

def count_paths_with_one_element(paths_with_counts):
    return sum(1 for path, count in paths_with_counts if count == 1)

def find_max_count(paths_with_counts):
    return max(count for path, count in paths_with_counts)

def create_tuples(paths):
    result_tuple = []
    for path in paths:
        split_path = path.split('|')
        result_tuple.append((split_path[-1], '/'.join(split_path[:-1])))
    return result_tuple

#parse_tree = '["C_major", ["D", ["D", ["S", ["N", "?"], "?"], "?"], "?"], ["T", "?"], ["Tp", ["S", ["D", "?"], ["Tg", "?"], "?"], "?"], ["T", "?"]]'
#parse_tree = '["C_major", ["vii°", ["iii", ["vii°", "?"], "?"], "?"]]'
#parse_tree = '["C_major", ["I", ["V", ["IV", ["vi", ["vii°", "?"], ["I", "?"], ["V", ["V", "?"], "?"], "?"], ["vii°", "?"], ["V", ["V", "?"], "?"], "?"], ["V", "?"], "?"], "?"]]'
#parse_tree = '["C_major", ["I", ["ii", "?"], "?"], ["I", "?"], ["ii", ["V", "?"], "?"]]'
#parse_tree = '["C_major", ["vi", ["vii°", ["vii°", ["iii", "?"], "?"], ["iii", "?"], "?"], ["vii°", "?"], ["iii", "?"], "?"]]'
#parse_tree = '["C_major", ["vi", "?"], ["iii", ["I", ["vi", "?"], ["IV", "?"], ["I", "?"], "?"], "?"], ["vi", "?"], ["I", "?"]]'
#parse_tree = '["C_major", ["iii", ["II7", "?"], "?"], ["V", "?"]]'
#parse_tree =  '["C_major", ["V", "?"], ["ii", ["V", ["ii", "?"], ["vii°7", "?"], "?"], "?"]]'
#parse_tree = '["C_major", ["I", "?"], ["I", ["V7", "?"], "?"], ["V", "?"], ["I", "?"]]'
#parse_tree = '["C", ["I", "?"], ["I", ["II7", ["iii", ["V", "?"], "?"], "?"], "?"], ["iii", ["V", ["II7", "?"], "?"], ["ii", "?"], "?"], ["V", "?"], ["I", "?"]]'
#parse_tree = '["C", ["I", "?"], ["I", ["iii", "?"], ["ii", ["iii", "?"], ["V", "?"], "?"], "?"], ["ii", ["V", "?"], "?"], ["V", "?"], ["I", "?"]]'
#parse_tree = '["C", ["I", "?"], ["V", ["ii", ["IV", "?"], ["ii", ["vii°", "?"], "?"], "?"], "?"], ["ii7", "?"], ["V", "?"], ["I", "?"]]'
parse_tree = '["C", ["I", "?"], ["#IV°7", ["vii°", ["I", "?"], ["iii", ["V", "?"], "?"], ["I", "?"], "?"], "?"], ["IV", "?"], ["V", "?"], ["I", "?"]]'

paths = parse_tree_to_paths(parse_tree)
paths_with_counts = count_elements_in_paths(paths)
one_element_count = count_paths_with_one_element(paths_with_counts)
max_count = find_max_count(paths_with_counts)
result_tuple = create_tuples(paths)

for path, count in paths_with_counts:
    print(f'{path} --> {count}')

print(f'\nBREADTH: Number of horizontal elements in the first layer: {one_element_count}')
print(f'DEPTH: Maximum count of vertical (nested) elements: {max_count}\n')
print(f'Resulting tuples: {result_tuple}\n')