import os
from itertools import permutations
from ast_tree_parser import parse_ast_tree
from pycparser import parse_file


def return_features_json(path: str = r'./test_dir/test.c') -> dict:
    ast_tree = parse_file(path, use_cpp=True, cpp_path='gcc',
                          cpp_args=['-E',
                                    r'-I./fake_libc_include',
                                    r'-I./test_dir'])
    return parse_ast_tree(ast_tree)


if __name__ == "__main__":
    print(return_features_json())
