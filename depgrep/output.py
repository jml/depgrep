
def common(xs, ys):
    if not xs or not ys:
        return 0
    for i, (x, y) in enumerate(zip(xs, ys)):
        if x != y:
            return i
    return i + 1


def _tree_format(data):
    last = []
    for datum in data:
        level = common(datum, last)
        datum_size = len(datum) - 1
        for new in datum[level:]:
            yield level, new, level == datum_size
            level += 1
        last = datum


def tree_format(output, data, sep, indent='  '):
    w = output.write
    data = sorted(datum.split(sep) for datum in data)
    for level, line, leaf in _tree_format(data):
        w(indent * level)
        if leaf:
            w('* ')
        else:
            w('- ')
        w(line)
        w('\n')
