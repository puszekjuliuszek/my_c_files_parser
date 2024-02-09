import os
import sys
sys.path.append("/".join(os.path.dirname(os.path.abspath(__file__)).split("/")[0:-1]))
from itertools import permutations
from ast_tree_parser import AST_Parser
from pycparser import parse_file


def return_features_json(path: str = r'./test_dir/test.c') -> dict:
    ast_tree = parse_file(path, use_cpp=True, cpp_path='gcc',
                          cpp_args=['-E',
                                    r'-I./fake_libc_include',
                                    r'-I./test_dir'])
    parser = AST_Parser()
    return parser.parse_ast_tree(ast_tree)


if __name__ == "__main__":
    print(return_features_json())
