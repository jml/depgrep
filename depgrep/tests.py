from testtools import TestCase
from testtools.matchers import Equals


def find_imports(python_code):
    return []


class TestImports(TestCase):

    def test_empty(self):
        imports = find_imports("")
        self.assertThat(imports, Equals([]))
