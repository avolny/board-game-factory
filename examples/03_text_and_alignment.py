from bgfactory import ff
import pangocffi as pango

w = 500
h = 350
padding = 60

container = ff.RoundedRectangle(0, 0, w, h, radius=60, stroke_width=15, stroke_src=(0.2, 0.3, 0.7),
                                fill_src=ff.COLOR_WHITE)

container.add(
    ff.TextUniform(
        padding, padding, w - 2 * padding, h - 2 * padding,
        "Hello from Board Game Factory!\n\nHow are you doing today?",
        fill_src=(0.2, 0.6, 0.9),
        stroke_width=1,
        stroke_src=ff.COLOR_BLACK,
        font_description=ff.FontDescription(
            family='Arial',
            size=w * 0.06,
            weight=pango.Weight.BOLD,
            style=pango.Style.ITALIC,
        ),
        halign=ff.HALIGN_CENTER,
        valign=ff.VALIGN_MIDDLE
    )
)

container.image().show()

container.image().save('assets/readme/example03.png')
