import textwrap
import _ast

from ast import iter_child_nodes, literal_eval


UNKNOWN_IMPORT = object()


def get_ast(python_code):
    return compile(
        textwrap.dedent(python_code), "<test>", "exec", _ast.PyCF_ONLY_AST)


def iter_imports(tree):
    for node in iter_child_nodes(tree):
        if isinstance(node, _ast.Import):
            for alias in node.names:
                yield alias.name
        elif isinstance(node, _ast.ImportFrom):
            module = node.module
            for alias in node.names:
                yield '%s.%s' % (module, alias.name)
        elif isinstance(node, _ast.Expr):
            if isinstance(node.value, _ast.Call):
                func = node.value.func
                if func.id == '__import__':
                    args = node.value.args
                    try:
                        module = literal_eval(args[0])
                    except ValueError:
                        yield UNKNOWN_IMPORT
                    else:
                        if len(args) >= 4:
                            froms = literal_eval(args[3])
                            for from_import in froms:
                                yield '%s.%s' % (module, from_import)
                        else:
                            yield module


def find_imports(python_code):
    """Find all of the imports in 'python_code'."""
    tree = get_ast(python_code)
    return list(iter_imports(tree))
