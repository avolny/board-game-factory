from PIL import Image
import cairocffi as cairo


def image_from_surface(surface):
    surface_cropped = cairo.ImageSurface(cairo.FORMAT_ARGB32, surface.get_width(), surface.get_height())
    cr = cairo.Context(surface_cropped)
    
    cr.rectangle(0, 0, surface_cropped.get_width(), surface_cropped.get_height())
    cr.set_source_surface(surface)
    cr.set_line_width(0)
    cr.fill()
    
    # print(surface.get_width())
    # print(surface.get_height())
    
    return Image.frombuffer(
        "RGBA", (surface_cropped.get_width(), surface_cropped.get_height()),
        surface_cropped.get_data(), "raw", "BGRA", 0, 1)


def adjust_rect_size_by_line_width(x, y, w, h, line_width):
    hw = line_width / 2
    return x + hw, y + hw, w - 2 * hw, h - 2 * hw