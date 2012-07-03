import textwrap
import _ast

from ast import iter_child_nodes


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


def find_imports(python_code):
    """Find all of the imports in 'python_code'."""
    tree = get_ast(python_code)
    return list(iter_imports(tree))
