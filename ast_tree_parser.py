from pycparser.c_ast import *

class AST_Parser():
    def __init__(self) -> None:
        self.pragma_loops = []
        self.loop_content = []
        self.loop_dependencies = []

    def get_main_content(self, ext):
        """zwraca zawartość maina"""
        for elem in ext:
            if elem.__class__ is FuncDef and elem.decl.name == 'main':
                return elem.body


    def get_info_about_arrays(self, block_items: list) -> list:
        """ przegląda wszystkie elementy maina i wybiera te które inicjalizują nowe tablice i zwraca info o nich"""
        # TODO pokrywamy tylko jeden case
        output = []
        for item in block_items:
            if item.__class__ is Decl and item.name.isupper() and len(item.name) == 1:
                name = item.name
                sizes = []
                for constat in item.init.args.exprs:
                    if constat.type == 'int':
                        sizes.append(int(constat.value))
                output.append((name, sizes))
        return output


    def dig_for_a_pragma_loop(self, item):
        """jeśli jest stmt przeglądamy block_items i jak jest w nich Pragma to ddaojemy kolejny elemnt do globalnej listy"""
        if hasattr(item, "stmt") and hasattr(item.stmt, "block_items"):
            for idx, item_inside in enumerate(item.stmt.block_items):
                if item_inside.__class__ is Pragma:
                    self.pragma_loops.append(item.stmt.block_items[idx + 1])
                    return True
                if item_inside.__class__ is For:
                    return self.dig_for_a_pragma_loop(item_inside)


    def get_pragma_loops(self, block_items: list) -> None:
        for item in block_items:
            if item.__class__ is For:
                self.dig_for_a_pragma_loop(item)

    def explore(self, node):
        method = 'explore_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_explore)
        return visitor(node)

    def generic_explore(self, node):
        print(f"[ERROR] NO DEFINED METHOD FOR {node.__class__.__name__}")
        print(node)

    def explore_ID(self, id):
        return id.name
    
    def explore_Constant(self, constant):
        if constant.type == 'int':
            return int(constant.value)
        else:
            return float(constant.value)

    def explore_ArrayRef(self, array_ref: ArrayRef) ->list:
        return ['ArrayRef', self.explore(array_ref.name), self.explore(array_ref.subscript)]
        
    def explore_BinaryOp(self, binary_op):
        left = self.explore(binary_op.left)
        right = self.explore(binary_op.right)
        return ['BinaryOp',left, right]

    def explore_dependencies(self, item, dependency_content):
        for assignment in item.block_items:
            array_access = ['Assignment']
            # lvalue
            array_access.append(self.explore(assignment.lvalue))

            # rvalue
            array_access.append(self.explore(assignment.rvalue))

            dependency_content.append(array_access)

    def get_loop_bounds(self, init, cond, next):
        name = init.lvalue.name
        start = int(init.rvalue.value)
        stop = int(cond.right.value)
        if next.op == 'p++':
            step = 1
        elif next == '++p':
            step = 1
        else:
            step = int(next.rvalue.value)
        return name, start, stop, step

    def explore_loop(self, loop, content, dependency_content):
        content.append(self.get_loop_bounds(loop.init, loop.cond, loop.next))
        if loop.stmt.__class__ is For:
            self.explore_loop(loop.stmt, content, dependency_content)
        if loop.stmt.__class__ is Compound:
            self.explore_dependencies(loop.stmt, dependency_content)
        return content, dependency_content

    def get_info_about_loops(self, block_items: list) -> list:
        """ przegląda wszystkie elementy maina i wybiera te które opisują pętle i zwraca info o nich"""
        output = []
        for item in block_items:
            output.append(self.explore_loop(item, [], []))
        return output

    def parse_ast_tree(self, ast_tree) -> dict:
        output = dict()
        main_body = self.get_main_content(ast_tree.ext)
        array_info = self.get_info_about_arrays(main_body.block_items)
        self.get_pragma_loops(main_body.block_items)
        loop_info = self.get_info_about_loops(self.pragma_loops)
        output['array_info'] = array_info
        output['loop_bounds'] = loop_info[0][0]
        output['data_deps'] = loop_info[0][1]

        return output
