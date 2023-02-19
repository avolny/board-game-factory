from bgfactory import ff
import pangocffi as pango

w = 400
h = 600

color = (0.2, 0.3, 0.7)

container = ff.RoundedRectangle(
    0, 0, w, h, radius=30, stroke_width=5, stroke_src=color, fill_src=ff.COLOR_WHITE,
    padding=(30, 30, 30, 30),
    layout=ff.VerticalFlowLayout(halign=ff.HALIGN_CENTER, valign=ff.VALIGN_TOP)
)

container.add(
    ff.TextUniform(
        0, 0, w * 0.8, ff.INFER,
        "Card Title",
        font_description=ff.FontDescription(
            family='Arial',
            size=w * 0.1,
            weight=pango.Weight.BOLD,
            style=pango.Style.NORMAL,
        ),
        halign=ff.HALIGN_CENTER,
        valign=ff.VALIGN_MIDDLE
    ),
    ff.TextUniform(
        0, 0, w * 0.8, ff.INFER,
        "This is a rather long card description. It contains multiple paragraphs that need to fit."
        "\n\nWhen I wrote this, I wasn't quite sure how much space this will take."
        "\n\nThat's when ff.INFER gets super handy!",
        font_description=ff.FontDescription(
            family='Arial',
            size=w * 0.05,
            weight=pango.Weight.NORMAL,
            style=pango.Style.OBLIQUE,
        ),
        halign=ff.HALIGN_LEFT,
        valign=ff.VALIGN_MIDDLE,
        margin=(0, h*0.1, 0, 0)
    ),
    ff.Container(
        0, 0, '100%', ff.FILL, layout=ff.HorizontalFlowLayout(halign=ff.HALIGN_CENTER, valign=ff.VALIGN_MIDDLE),
        children=[
            ff.RegularPolygon(0, 0, h * 0.05, num_points=3, rotation=1, fill_src=ff.COLOR_TRANSPARENT, stroke_src=color),
            ff.RegularPolygon(0, 0, h * 0.05, num_points=3, rotation=0, fill_src=ff.COLOR_TRANSPARENT, stroke_src=color),
            ff.RegularPolygon(0, 0, h * 0.05, num_points=3, rotation=1, fill_src=ff.COLOR_TRANSPARENT, stroke_src=color)
        ]
    )
)

container.image().show()

container.image().save('assets/readme/example04.png')
