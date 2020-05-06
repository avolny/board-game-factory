from PIL.ImageDraw import ImageDraw


def rounded_rectangle(self: ImageDraw, xy, corner_radius, outline=None, width=1):
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
        width=width
    )
    self.arc([(bottom_right_point[0] - corner_radius * 2, bottom_right_point[1] - corner_radius * 2), bottom_right_point],
        0,
        90,
        fill=outline,
        width=width
    )
    self.arc([(upper_left_point[0], bottom_right_point[1] - corner_radius * 2), (upper_left_point[0] + corner_radius * 2, bottom_right_point[1])],
        90,
        180,
      fill=outline,
        width=width
    )
    self.arc([(bottom_right_point[0] - corner_radius * 2, upper_left_point[1]), (bottom_right_point[0], upper_left_point[1] + corner_radius * 2)],
        270,
        360,
        fill=outline,
        width=width
    )


ImageDraw.rounded_rectangle = rounded_rectangle