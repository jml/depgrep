from testtools import TestCase
from testtools.matchers import SameMembers


def find_imports(python_code):
    """Find all of the imports in 'python_code'."""
    imports = []
    for line in python_code.splitlines():
        if line.startswith('import '):
            modules = [m.strip() for m in line[7:].split(',')]
            imports.extend(modules)
        if line.startswith('from '):
            start, end = line[5:].split(' import ')
            imports.extend(
                ['%s.%s' % (start, m.strip()) for m in end.split(',')])
    return imports


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
