from PIL import Image, ImageDraw, ImageFont


class TextOverflowException(Exception):
    pass


def draw_text(
    text: str,
    font_size: float,
    width: int,
    height: int,
    text_color: tuple[int, int, int],
    bg_color: tuple[int, int, int],
    margin_correction: int,
    rotate: int = 0,
) -> Image:
    rect_image = Image.new("RGB", (width, height), bg_color)
    font = ImageFont.truetype("Futura.ttc", font_size)
    draw = ImageDraw.Draw(rect_image)
    _, _, w, h = draw.textbbox((0, 0), text, font=font)
    text_x_pos, text_y_pos = ((width - w) / 2, (height - h) / 2 - margin_correction)
    if text_x_pos < 0:
        raise TextOverflowException(f"WARNING: '{text}' is too long!")
    draw.text((text_x_pos, text_y_pos), text, font=font, fill=text_color, align="center")
    return rect_image.rotate(rotate, expand=1) if rotate else rect_image
