from bgfactory import ff

# colors can be 3-tuple or 4-tuple of values between 0 and 1
COLOR1 = (232 / 255, 131 / 255, 7 / 255)
COLOR2 = (33 / 255, 196 / 255, 131 / 255)
COLOR3 = (32 / 255, 65 / 255, 212 / 255)
COLOR4_SEMITRANSPARENT = (32 / 255, 65 / 255, 212 / 255, 128 / 255)
COLOR5_SEMITRANSPARENT = (180 / 255, 60 / 255, 64 / 255, 128 / 255)

# for shapes: stroke = border, fill = inside
container = ff.Container(
    0, 0, 400, 400,
    children=[
        ff.Rectangle(50, 50, 350, 350, fill_src=ff.COLOR_WHITE, stroke_width=0),
        ff.Line(20, 380, 380, 20, stroke_width=5, stroke_src=COLOR3),
        ff.Circle(140, 140, 80, stroke_width=5, stroke_src=COLOR1, fill_src=COLOR2),
        ff.RoundedRectangle(20, 20, 230, 230, stroke_width=5, stroke_src=COLOR1, fill_src=ff.COLOR_TRANSPARENT),
    ]
)
container.add(
    ff.RegularPolygon(130, 260, 40, 5, fill_src=COLOR4_SEMITRANSPARENT, stroke_width=0),
    ff.RegularPolygon(160, 220, 80, 6, fill_src=COLOR5_SEMITRANSPARENT, stroke_width=0)
)

container.image().show()

container.image().save('assets/readme/example02.png')