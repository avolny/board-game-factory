def parse_percent(val):
    return float(val[:-1]) / 100


def is_percent(val):
    return isinstance(val, str) and val[-1] == '%'


def perc(val):
    return '{:d}%'.format(val)