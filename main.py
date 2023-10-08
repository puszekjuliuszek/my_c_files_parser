import os
from itertools import permutations
from ast_tree_parser import parse_ast_tree
from pycparser import parse_file


def return_features_json(path: str = './test_dir/test.c') -> dict:
    ast_tree = parse_file(path, use_cpp=True, cpp_path='gcc',
                          cpp_args=['-E', r'-ID:\prywatne\jul\pycparser\utils\fake_libc_include',
                                    r'-ID:\Prywatne\jul\python_projekty\c_files_parser\test_dir'])
    return parse_ast_tree(ast_tree)


if __name__ == "__main__":
    return_features_json()
