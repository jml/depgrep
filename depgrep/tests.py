from testtools import TestCase
from testtools.matchers import SameMembers

from .scanner import find_imports


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


# TODO: Actually use a Python syntax parser.

# TODO: Support multi-line 'from foo import (...)' style imports

# TODO: For found imports, distinguish which part is the module and which part
# is the name within the module. (use sys.path)

# TODO: Command-line script

# TODO: Show files for found modules (use sys.path)

# TODO: Recursively search many files and generate a set of all things that
# they import that are outside that set of files.  (Preserve which file
# imports what).

# TODO: Search the sys.path to find things that import X.

# XXX: Not sure what to do about imports in function definitions, for example.

