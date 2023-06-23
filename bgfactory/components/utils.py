import re


def parse_percent(val):
    return float(val[:-1]) / 100


def add_percent(val1, val2):
    return '{}%'.format((parse_percent(val1) + parse_percent(val2)) * 100)


def is_percent(val):
    return isinstance(val, str) and val[-1] == '%'


def perc(val):
    return '{:d}%'.format(val)


A4_WIDTH_MM = 210
A4_HEIGHT_MM = 297

MM_PER_INCH = 25.4


def mm_to_pixels(mm, dpi=300):
    return int(mm / MM_PER_INCH * dpi)


def get_a4_pixel_size(dpi=300):
    return mm_to_pixels(A4_WIDTH_MM, dpi), mm_to_pixels(A4_HEIGHT_MM, dpi)


def hex_color_to_rgba(hex):
    match = re.match(r'^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$', hex, re.IGNORECASE)
    if not match:
        raise ValueError('Invalid hex color: "{}"'.format(hex))

    r, g, b = match.group(1), match.group(2), match.group(3)

    return int(r, 16) / 255, int(g, 16) / 255, int(b, 16) / 255, 255 / 255
