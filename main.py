import os
import sys

THIS_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(THIS_DIR_PATH)
from itertools import permutations
from ast_tree_parser import AST_Parser
from pycparser import parse_file


def return_features_json(path: str = r'./test_dir/test.c', additional_paths=None) -> dict:
    if additional_paths is None:
        additional_paths = []
    additional_paths += ['-E', f'-I{THIS_DIR_PATH}/fake_libc_include', f'-I{THIS_DIR_PATH}/test_dir']
    ast_tree = parse_file(path, use_cpp=True, cpp_path='gcc',
                          cpp_args=additional_paths)
    parser = AST_Parser()
    return parser.parse_ast_tree(ast_tree)


if __name__ == "__main__":
    print(return_features_json())


