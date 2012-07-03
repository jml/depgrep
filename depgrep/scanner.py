


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
