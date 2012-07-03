from testtools import TestCase
from testtools.matchers import Equals, SameMembers

from .scanner import find_imports, UNKNOWN_IMPORT
from .output import _tree_format, common


class TestImports(TestCase):

    def test_empty(self):
        imports = find_imports("")
        self.assertThat(imports, SameMembers([]))

    def test_import(self):
        imports = find_imports("import foo\n")
        self.assertThat(imports, SameMembers(['foo']))

    def test_multi_import(self):
        imports = find_imports("import foo, bar\n")
        self.assertThat(imports, SameMembers(['foo', 'bar']))

    def test_from_import(self):
        imports = find_imports("from foo import bar")
        self.assertThat(imports, SameMembers(['foo.bar']))

    def test_multi_from_import(self):
        imports = find_imports("from foo import bar, baz")
        self.assertThat(imports, SameMembers(['foo.bar', 'foo.baz']))

    def test_multiline_from_import(self):
        imports = find_imports("""
from foo import (
    bar,
    baz,
)
""")
        self.assertThat(imports, SameMembers(['foo.bar', 'foo.baz']))

    def test_manual_import(self):
        imports = find_imports('__import__("foo")')
        self.assertThat(imports, SameMembers(['foo']))

    def test_manual_import_variable(self):
        imports = find_imports('__import__(foo)')
        self.assertThat(imports, SameMembers([UNKNOWN_IMPORT]))

    def test_manual_from_import(self):
        imports = find_imports(
            '__import__("foo", globals(), locals(), ["bar", "baz"])')
        self.assertThat(imports, SameMembers(['foo.bar', 'foo.baz']))

    def test_manual_from_import_variable(self):
        imports = find_imports(
            '__import__("foo", globals(), locals(), [bar, "baz"])')
        self.assertThat(imports, SameMembers(['foo']))


class TestIterPythonFiles(TestCase):

    # Given a Python file named '*.py', include that.
    # Given a directory find all Python files:
    # - either named '*.py'
    # Given a module name, get the file for that
    # Given a package name, find all the modules

    pass



class TestCommon(TestCase):
    
    def test_equal_lists(self):
        x = [1, 2, 3, 4]
        self.assertEqual(len(x), common(x, x))

    def test_sublist(self):
        x = [1, 2, 3, 4]
        self.assertEqual(2, common(x, x[:2]))

    def test_fork(self):
        x = [1, 2, 3, 4]
        y = [1, 2, 5, 6]
        self.assertEqual(2, common(x, y))

    def test_empty(self):
        self.assertEqual(0, common([], []))

    def test_different(self):
        x = [2, 3, 4, 5]
        y = [1, 2, 3, 4]
        self.assertEqual(0, common(x, y))


class TestTreeOutput(TestCase):

    def test_one_level(self):
        output = list(_tree_format(['foo', 'bar'], sep='.'))
        self.assertThat(output, Equals([(0, 'foo'), (0, 'bar')]))

    def test_two_level(self):
        output = list(_tree_format(['foo.bar', 'foo.baz'], sep='.'))
        self.assertThat(output, Equals([(0, 'foo'), (1, 'bar'), (1, 'baz')]))

    def test_two_branches(self):
        output = list(_tree_format(['foo.bar', 'foo.baz', 'qux.bar'], sep='.'))
        self.assertThat(output, Equals([(0, 'foo'), (1, 'bar'), (1, 'baz'),
                                        (0, 'qux'), (1, 'bar')]))

    def test_deeper_branches(self):
        output = list(_tree_format(['foo.bar', 'foo.baz.qux', 'foo.bop'], sep='.'))
        self.assertThat(output, Equals([(0, 'foo'), (1, 'bar'), (1, 'baz'),
                                        (2, 'qux'), (1, 'bop')]))



# TODO: For found imports, distinguish which part is the module and which part
# is the name within the module. (use sys.path)

# TODO: Command-line script

# TODO: Show files for found modules (use sys.path)

# TODO: Recursively search many files and generate a set of all things that
# they import that are outside that set of files.  (Preserve which file
# imports what).

# TODO: Search the sys.path to find things that import X.

# XXX: Not sure what to do about imports in function definitions, for example.

# TODO: Handle from-style imports using __import__

# TODO: Distinguish between used imports and unused imports.

# TODO: Tree-style output
