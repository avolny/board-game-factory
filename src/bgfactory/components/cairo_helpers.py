from PIL import Image


def image_from_surface(surface):
    return Image.frombuffer(
        "RGBA", (surface.get_width(), surface.get_height()),
        surface.get_data(), "raw", "BGRA", 0, 1)


def adjust_rect_size_by_line_width(x, y, w, h, line_width):
    hw = line_width / 2
    return x + hw, y + hw, w - 2 * hw, h - 2 * hw