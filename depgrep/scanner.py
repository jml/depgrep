import textwrap
import ast


UNKNOWN_IMPORT = object()


def get_ast(python_code):
    return ast.parse(textwrap.dedent(python_code), "<test>")


class ImportFinder(ast.NodeVisitor):

    def __init__(self, got_import):
        self.got_import = got_import

    def visit_Import(self, node):
        for alias in node.names:
            self.got_import(alias.name)

    def visit_ImportFrom(self, node):
        module = node.module
        for alias in node.names:
            self.got_import('%s.%s' % (module, alias.name))

    def visit_Call(self, node):
        if getattr(node.func, 'id', None) != '__import__':
            return self.generic_visit(node)
        args = node.args
        try:
            module = ast.literal_eval(args[0])
        except ValueError:
            self.got_import(UNKNOWN_IMPORT)
        else:
            if len(args) >= 4:
                try:
                    froms = ast.literal_eval(args[3])
                except ValueError:
                    self.got_import(module)
                else:
                    for from_import in froms:
                        self.got_import('%s.%s' % (module, from_import))
            else:
                self.got_import(module)


def find_imports(python_code):
    """Find all of the imports in 'python_code'."""
    imports = []
    tree = get_ast(python_code)
    finder = ImportFinder(imports.append)
    finder.visit(tree)
    return imports
