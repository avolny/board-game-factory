from math import pi

import cairo
from PIL import Image
from PIL.ImageDraw import ImageDraw


def draw_filled_round_rect(cr, area, width, radius, clr_border, clr_fill):
    cr.set_line_width(width)

    hw = width / 2

    (a, b), (c, d) = area
    a += hw
    b += hw
    c -= hw
    d -= hw

    cr.arc(a + radius, b + radius, radius, 2 * (pi / 2), 3 * (pi / 2))
    cr.arc(c - radius, b + radius, radius, 3 * (pi / 2), 4 * (pi / 2))
    cr.arc(c - radius, d - radius, radius, 0 * (pi / 2), 1 * (pi / 2))  # ;o)
    cr.arc(a + radius, d - radius, radius, 1 * (pi / 2), 2 * (pi / 2))
    cr.close_path()

    cr.set_source_rgba(*clr_fill)
    cr.fill_preserve()
    cr.set_source_rgba(*clr_border)
    cr.stroke()


def draw_rounded_rectangle(w, h, xy, radius, outline, fill, width=1):
    
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    cr = cairo.Context(surface)
    
    draw_filled_round_rect(cr, xy, width, radius, outline, fill)

    im = Image.frombuffer("RGBA",
                          (w, h),
                          surface.get_data().tobytes(),
                          "raw",
                          "BGRA",
                          0, 1)
    
    return im






def rounded_rectangle_old(self: ImageDraw, xy, corner_radius, outline=None, width=1):
    upper_left_point = xy[0]
    bottom_right_point = xy[1]
    self.line(
        [
            (upper_left_point[0] + corner_radius, upper_left_point[1]),
            (bottom_right_point[0] - corner_radius, upper_left_point[1]),
        ],
        fill=outline,
        width=width
    )
    self.line(
        [
            (upper_left_point[0] + corner_radius, bottom_right_point[1]),
            (bottom_right_point[0] - corner_radius, bottom_right_point[1]),
        ],
        fill=outline,
        width=width
    )
    self.line(
        [
            (upper_left_point[0], upper_left_point[1] + corner_radius),
            (upper_left_point[0], bottom_right_point[1] - corner_radius),
        ],
        fill=outline,
        width=width
    )
    self.line(
        [
            (bottom_right_point[0], upper_left_point[1] + corner_radius),
            (bottom_right_point[0], bottom_right_point[1] - corner_radius),
        ],
        fill=outline,
        width=width
    )
    
    self.arc([upper_left_point, (upper_left_point[0] + corner_radius * 2, upper_left_point[1] + corner_radius * 2)],
        180,
        270,
        fill=outline,
        width=int(math.ceil(width/2))
    )
    self.arc([(bottom_right_point[0] - corner_radius * 2, bottom_right_point[1] - corner_radius * 2), bottom_right_point],
        0,
        90,
        fill=outline,
        width=int(math.ceil(width/2))
    )
    self.arc([(upper_left_point[0], bottom_right_point[1] - corner_radius * 2), (upper_left_point[0] + corner_radius * 2, bottom_right_point[1])],
        90,
        180,
      fill=outline,
        width=int(math.ceil(width/2))
    )
    self.arc([(bottom_right_point[0] - corner_radius * 2, upper_left_point[1]), (bottom_right_point[0], upper_left_point[1] + corner_radius * 2)],
        270,
        360,
        fill=outline,
        width=int(math.ceil(width/2))
    )


# ImageDraw.rounded_rectangle = rounded_rectangle