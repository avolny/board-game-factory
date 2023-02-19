from bgfactory import ff
import pangocffi as pango

CARD_WIDTH_MM = 63
CARD_HEIGHT_MM = 88
CARD_RADIUS_MM = 3
DPI = 300

class MyCard(ff.RoundedRectangle):

    def __init__(self, x, y, title, description, color=(0.2, 0.3, 0.7)):
        pad = 25

        super(MyCard, self).__init__(
            x, y, ff.mm_to_pixels(CARD_WIDTH_MM, DPI), ff.mm_to_pixels(CARD_HEIGHT_MM, DPI),
            radius=ff.mm_to_pixels(CARD_RADIUS_MM), stroke_width=5,
            stroke_src=color, fill_src=ff.COLOR_WHITE, padding=(pad, pad, pad, pad),
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
                valign=ff.VALIGN_MIDDLE
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

cards = []

for i in range(5):
    cards.append(
        MyCard(
            0, 0,
            'Warlock',
            'Warlocks are powerful users of magic. It is ancient and its origins are so old that they were long forgotten.'
            '\n\nIt was once said, by a particular man, in a particular spot, that in order to find the origin warlock'
            ' magic, you have to go to the beginning of time, take a right turn, and continue until the edge of space.'
            ' Those who heard it were as confused as you are.\n\nDespite their power, Warlocks are typically cheerful '
            'people, armed with an unexpected arsenal of dad jokes.'
        ),
    )

for i in range(5):
    cards.append(
        MyCard(
            0, 0,
            'Rogue',
            'Rogues are smart as they are sneaky. They can steal your wallet, your life but also, and not many '
            'people know this, also your wife.\n\nThere have been accounts of rogues breaking into a house for a job '
            'only to leave with the homeowner\'s wife instead of the loot, never to be found again (though probably'
            ' somewhere on the Canary Islands).',
            color=(0.2, 0.7, 0.3)
        ),
    )

# set your page margins in your program before printing to make sure you get exact measurments on the print
# you can use GIMP to check the actual DPI that's gonna be printed with to see if you have setup everything properly
sheets = ff.make_printable_sheets(cards, dpi=DPI, print_margin_hor_mm=5, print_margin_ver_mm=5)

#sheets = ff.make_printable_sheets(cards, dpi=DPI, print_margin_hor_mm=5, print_margin_ver_mm=5, out_dir_path='sheets')

for sheet in sheets:
    sheet.image().show()


i = 1
for sheet in sheets:
    sheet.image().save(f'assets/readme/example06_{i}.png')
    i += 1