import cairocffi as cairo
import numpy as np

from bgfactory.components.constants import COLOR_BLACK, COLOR_WHITE
from bgfactory.components.shape import Shape


class RegularPolygon(Shape):

    def __init__(self, x, y, num_points, radius, rotation=0, fill_src=COLOR_WHITE, stroke_width=5,
                 stroke_src=COLOR_BLACK, **kwargs):
        self.radius = radius
        self.rotation = rotation
        self.num_points = num_points

        self.points = self.generate_polygon_points_and_calc_dims(self.num_points, self.radius, self.rotation)
        self.points, w, h = self.adjust_polygon_points_and_compute_dims(self.points)

        super(RegularPolygon, self).__init__(
            x, y, w, h, stroke_width=stroke_width, stroke_src=stroke_src, fill_src=fill_src, **kwargs)

    def _draw(self, surface: cairo.Surface, w, h):
        cr = cairo.Context(surface)

        adj_delta = self.stroke_width * 1

        points = self.generate_polygon_points_and_calc_dims(self.num_points, self.radius - adj_delta, self.rotation)
        points, _, _ = self.adjust_polygon_points_and_compute_dims(points)

        for i in range(len(points)):
            x, y = points[i]
            points[i] = x + adj_delta, y + adj_delta

        cr.move_to(*points[0])
        for i in range(1, len(points)):
            cr.line_to(*points[i])

        cr.line_to(*points[0])
        cr.close_path()

        self.stroke_and_fill(cr, w, h)

    def get_nth_point_relative_coords(self, n):
        """
        The first point is the bottom one, or if lying flat, the bottom right one.
        :param n: index of point, from 0 to self.num_points - 1
        :return:
        """
        return self.points[n]

    @classmethod
    def adjust_polygon_points_and_compute_dims(cls, points, extra_offset=0):
        minx = maxx = points[0][0]
        miny = maxy = points[0][1]

        for pointx, pointy in points:
            miny = min(pointy, miny)
            minx = min(pointx, minx)
            maxy = max(pointy, maxy)
            maxx = max(pointx, maxx)

        new_points = []
        for pointx, pointy in points:
            new_points.append((pointx - minx + extra_offset, pointy - miny + extra_offset))

        width = maxx - minx
        height = maxy - miny

        return new_points, width, height

    @classmethod
    def generate_polygon_points_and_calc_dims(cls, num_points, radius, rotation):

        if num_points < 3:
            raise ValueError(f'Can only generate regular polygons for 3+ points. {num_points=}')

        step_angle = 2 * np.pi / num_points

        half_step_angle = step_angle / 2

        starting_angle = np.pi / 2 + (1 - rotation) * half_step_angle
        point_angle = starting_angle % (2 * np.pi)

        points = []

        for i in range(num_points):
            pointx = np.cos(point_angle) * radius
            pointy = np.sin(point_angle) * radius

            points.append((pointx, pointy))

            point_angle = (point_angle + step_angle) % (2 * np.pi)

        return points


if __name__ == '__main__':
    from bgfactory.components.shape import Rectangle

    num_sides = [3, 5, 6, 8, 10, 12]
    rotations = np.linspace(0, 1, 5)

    rows = len(num_sides)
    cols = len(rotations)

    shape_side = 100
    spacing = 15

    sheet = Rectangle(0, 0, (shape_side + spacing) * cols + spacing, (shape_side + spacing) * rows + spacing,
                      stroke_width=0)

    start_color = (0.9, 0.8, 0.1)
    end_color = (0.1, 0.8, 0.9)

    for i in range(rows):
        for j in range(cols):
            imix = i / (rows - 1)
            jmix = j / (cols - 1)

            red_channel = (end_color[0] - start_color[0]) * imix + start_color[0]
            blue_channel = (end_color[2] - start_color[2]) * jmix + start_color[2]

            color = (red_channel, 0.5, blue_channel)

            sheet.add(
                RegularPolygon(
                    shape_side * j + spacing * (j + 1),
                    shape_side * i + spacing * (i + 1),
                    num_points=num_sides[i],
                    radius=shape_side / 2,
                    rotation=rotations[j],
                    stroke_width=3,
                    stroke_src=color
                )
            )

    # poly = RegularPolygon(0, 0, 3, 150, rotation=1, stroke_src=COLOR_RED)
    # poly.image().show()

    sheet.image().show()
