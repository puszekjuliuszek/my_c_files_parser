from pycparser.c_ast import *

pragma_loops = []


def get_main_content(ext):
    """zwraca zawartość maina"""
    for elem in ext:
        if elem.__class__ is FuncDef and elem.decl.name == 'main':
            return elem.body


def get_info_about_arrays(block_items: list) -> list:
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


def dig_for_a_pragma_loop(item):
    """jeśli jest stmt przeglądamy block_items i jak jest w nich Pragma to ddaojemy kolejny elemnt do globalnej listy"""
    if hasattr(item, "stmt") and hasattr(item.stmt, "block_items"):
        for idx, item_inside in enumerate(item.stmt.block_items):
            if item_inside.__class__ is Pragma:
                pragma_loops.append(item.stmt.block_items[idx + 1])
                return True
            if item_inside.__class__ is For:
                return dig_for_a_pragma_loop(item_inside)


def get_pragma_loops(block_items: list) -> None:
    for item in block_items:
        if item.__class__ is For:
            dig_for_a_pragma_loop(item)


def get_loop_bounds(init, cond, next):
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


def explore_loop(loop, content, dependency_content):
    content.append(get_loop_bounds(loop.init, loop.cond, loop.next))
    if loop.stmt.__class__ is For:
        explore_loop(loop.stmt, content, dependency_content)
    if loop.stmt.__class__ is Compound:
        explore_dependencies(loop.stmt, dependency_content)
    return content, dependency_content

def explore_array_ref(array_ref: ArrayRef) ->list:
    if array_ref.name.__class__ is ArrayRef:
        return explore_array_ref(array_ref.name) + [array_ref.subscript.name]
    elif array_ref.name.__class__ is ID:
        return [array_ref.name.name, array_ref.subscript.name]


def get_info_about_loops(block_items: list) -> list:
    """ przegląda wszystkie elementy maina i wybiera te które opisują pętle i zwraca info o nich"""
    output = []
    for item in block_items:
        output.append(explore_loop(item, [], []))
    return output


def explore_binary_op(binary_op, content):
    # TODO case z i+5
    # left
    if binary_op.left.__class__ is BinaryOp:
        explore_binary_op(binary_op.left, content)
    elif binary_op.left.__class__ is ArrayRef:
        content.append(explore_array_ref(binary_op.left))

    # right
    if binary_op.right.__class__ is BinaryOp:
        explore_binary_op(binary_op.right, content)
    elif binary_op.right.__class__ is Constant:
        # TODO int czy float?
        content.append(int(binary_op.right.value))
    elif binary_op.right.__class__ is ArrayRef:
        content.append(explore_array_ref(binary_op.right))

def explore_dependencies(item, dependency_content):
    for assignment in item.block_items:
        array_access = []
        # lvalue
        array_access.append(explore_array_ref(assignment.lvalue))

        # rvalue
        if assignment.rvalue.__class__ is BinaryOp:
            explore_binary_op(assignment.rvalue, array_access)
        elif assignment.rvalue.__class__ is ArrayRef:
            array_access.append(explore_array_ref(assignment.rvalue))
        dependency_content.append(array_access)


def parse_ast_tree(ast_tree) -> dict:
    output = dict()
    main_body = get_main_content(ast_tree.ext)
    array_info = get_info_about_arrays(main_body.block_items)
    get_pragma_loops(main_body.block_items)
    loop_info = get_info_about_loops(pragma_loops)
    output['array_info'] = array_info
    output['loop_bounds'] = loop_info[0][0]
    output['data_deps'] = loop_info[0][1]

    return output
