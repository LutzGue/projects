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

#parse_tree = '["C_major", ["D", ["D", ["S", ["N", "?"], "?"], "?"], "?"], ["T", "?"], ["Tp", ["S", ["D", "?"], ["Tg", "?"], "?"], "?"], ["T", "?"]]'
#parse_tree = '["C_major", ["vii°", ["iii", ["vii°", "?"], "?"], "?"]]'
#parse_tree = '["C_major", ["I", ["V", ["IV", ["vi", ["vii°", "?"], ["I", "?"], ["V", ["V", "?"], "?"], "?"], ["vii°", "?"], ["V", ["V", "?"], "?"], "?"], ["V", "?"], "?"], "?"]]'
#parse_tree = '["C_major", ["I", ["ii", "?"], "?"], ["I", "?"], ["ii", ["V", "?"], "?"]]'
parse_tree = '["C_major", ["vi", ["vii°", ["vii°", ["iii", "?"], "?"], ["iii", "?"], "?"], ["vii°", "?"], ["iii", "?"], "?"]]'

print(parse_tree_to_paths(parse_tree))
