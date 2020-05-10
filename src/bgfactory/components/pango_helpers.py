from bgfactory.components.constants import HALIGN_LEFT, HALIGN_CENTER, HALIGN_RIGHT
import pangocffi as pango


PANGO_SCALE = 1024


def convert_to_pango_align(halign):
    if halign == HALIGN_LEFT:
        return pango.Alignment.LEFT
    elif halign == HALIGN_CENTER:
        return pango.Alignment.CENTER
    elif halign == HALIGN_RIGHT:
        return pango.Alignment.RIGHT
    else:
        raise ValueError('Horizontal alignment type {} not recognized'.format(halign))