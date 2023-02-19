from bgfactory import ff
import pangocffi as pango

CARD_WIDTH = 400
CARD_HEIGHT = 600


class MyCard(ff.RoundedRectangle):

    def __init__(self, x, y, title, description, color=(0.2, 0.3, 0.7)):
        pad = 25

        super(MyCard, self).__init__(
            x, y, CARD_WIDTH, CARD_HEIGHT, radius=30, stroke_width=5, stroke_src=color, fill_src=ff.COLOR_WHITE,
            padding=(pad, pad, pad, pad),
            layout=ff.VerticalFlowLayout(halign=ff.HALIGN_CENTER, valign=ff.VALIGN_TOP)
        )

        self.add(
            ff.TextUniform(
                0, 0, self.w * 0.8, ff.INFER,
                title,
                font_description=ff.FontDescription(
                    family='Arial',
                    size=self.w * 0.1,
                    weight=pango.Weight.BOLD,
                    style=pango.Style.NORMAL,
                ),
                halign=ff.HALIGN_CENTER,
                valign=ff.VALIGN_MIDDLE,
            )
        )

        self.add(
            ff.TextUniform(
                0, 0, self.w * 0.8, ff.INFER,
                description,
                font_description=ff.FontDescription(
                    family='Arial',
                    size=self.w * 0.045,
                    weight=pango.Weight.NORMAL,
                    style=pango.Style.OBLIQUE,
                ),
                halign=ff.HALIGN_LEFT,
                valign=ff.VALIGN_MIDDLE,
                margin=(0, pad, 0, pad)
            )
        )

        bottom_panel = ff.Container(
            0, 0, '100%', ff.FILL, layout=ff.HorizontalFlowLayout(halign=ff.HALIGN_CENTER, valign=ff.VALIGN_MIDDLE)
        )

        bottom_panel.add(
            ff.RegularPolygon(0, 0, self.h * 0.05, num_points=3, rotation=1, fill_src=ff.COLOR_TRANSPARENT,
                              stroke_src=color),
            ff.RegularPolygon(0, 0, self.h * 0.05, num_points=3, rotation=0, fill_src=ff.COLOR_TRANSPARENT,
                              stroke_src=color),
            ff.RegularPolygon(0, 0, self.h * 0.05, num_points=3, rotation=1, fill_src=ff.COLOR_TRANSPARENT,
                              stroke_src=color)
        )

        self.add(bottom_panel)


container = ff.Container(
    0, 0, 2 * CARD_WIDTH, CARD_HEIGHT
)

container.add(
    MyCard(
        0, 0,
        'Warlock',
        'Warlocks are powerful users of magic. It is ancient and its origins are so old that they were long forgotten.'
        '\n\nIt was once said, by a particular man, in a particular spot, that in order to find the origin warlock'
        ' magic, you have to go to the beginning of time, take a right turn, and continue until the edge of space.'
        ' Those who heard it were as confused as you are.\n\nDespite their power, Warlocks are typically cheerful '
        'people, armed with an unexpected arsenal of dad jokes.'
    ),
    MyCard(
        CARD_WIDTH, 0,
        'Rogue',
        'Rogues are smart as they are sneaky. They can steal your wallet, your life but also, and not many '
        'people know this, also your wife.\n\nThere have been accounts of rogues breaking into a house for a job '
        'only to leave with the homeowner\'s wife instead of the loot, never to be found again (though probably'
        ' somewhere on the Canary Islands).',
        color=(0.2, 0.7, 0.3)
    ),
)

container.image().show()

container.image().save('assets/readme/example05.png')
