
def common(xs, ys):
    if not xs or not ys:
        return 0
    for i, (x, y) in enumerate(zip(xs, ys)):
        if x != y:
            return i
    return i + 1


def _tree_format(data, sep):
    last = []
    for datum in data:
        this = datum.split(sep)
        level = common(this, last)
        for new in this[level:]:
            yield level, new
            level += 1
        last = this


def tree_format(data, sep, indent='  '):
    return '\n'.join(
        indent * level + line for level, line in _tree_format(data, sep)) + '\n'
