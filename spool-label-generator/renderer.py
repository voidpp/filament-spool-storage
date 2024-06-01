from PIL import Image

from contants import dpi
from tools import draw_text, TextOverflowException
from types_ import Filament, Config


def render_filament_labels(filaments: list[Filament], config: Config, output_file_basename: str):
    cursor_x_pos = config.paper.margin
    cursor_y_pos = config.paper.margin
    current_image = None
    image_index = 0

    for idx, filament in enumerate(filaments):
        if cursor_y_pos + config.label.height > config.paper.height or idx == len(filaments) - 1:
            if current_image is None:
                raise Exception("WTF?")
            filename = f"{output_file_basename}-{image_index}.png"
            current_image.save(filename, dpi=(dpi, dpi))
            print(f"{filename} saved.")
            current_image.close()
            current_image = None
            image_index += 1

        if current_image is None:
            current_image = Image.new("RGB", (config.paper.width, config.paper.height), (255, 255, 255))
            cursor_x_pos = config.paper.margin
            cursor_y_pos = config.paper.margin

        type_desc = config.types[filament.type]

        if cursor_x_pos + config.label.width > config.paper.width + 1:
            cursor_x_pos = config.paper.margin
            cursor_y_pos += config.label.height

        remaining_label_width = config.label.width

        type_text = draw_text(
            type_desc.label,
            config.label.type.font_size,
            config.label.height,
            config.label.type.width,
            (255, 255, 255),
            type_desc.color,
            config.label.type.margin_correction,
            90,
        )
        current_image.paste(type_text, (cursor_x_pos, cursor_y_pos))
        cursor_x_pos += config.label.type.width
        remaining_label_width -= config.label.type.width

        if filament.sub_type:
            subtype_text = draw_text(
                filament.sub_type.upper(),
                config.label.subtype.font_size,
                config.label.height,
                config.label.subtype.width,
                (0, 0, 0),
                (255, 255, 255),
                config.label.subtype.margin_correction,
                90,
            )
            current_image.paste(subtype_text, (cursor_x_pos, cursor_y_pos))
            cursor_x_pos += config.label.subtype.width
            remaining_label_width -= config.label.subtype.width

        for name in filament.render_name():
            try:
                name_text = draw_text(
                    name,
                    config.label.name.font_size,
                    remaining_label_width,
                    config.label.height,
                    (255, 255, 255),
                    (0, 0, 0),
                    config.label.name.margin_correction,
                    0,
                )
                current_image.paste(name_text, (cursor_x_pos, cursor_y_pos))
                cursor_x_pos += remaining_label_width
                break
            except TextOverflowException:
                continue
        else:
            raise Exception(f"Could not render name for {filament}. Stopping.")
