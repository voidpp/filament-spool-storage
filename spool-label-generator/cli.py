from argparse import ArgumentParser
from pathlib import Path

from PIL import Image

from contants import dpi
from funcs import draw_text
from types_ import load_filaments, load_config

parser = ArgumentParser()
parser.add_argument("filaments", type=Path)
parser.add_argument("-c", "--config", type=Path, default="config.yaml")

cli_args = parser.parse_args()

filaments_file_path: Path = cli_args.filaments

filaments = load_filaments(filaments_file_path)
config = load_config(cli_args.config)

image = Image.new("RGB", (config.paper.width, config.paper.height), (255, 255, 255))

cursor_x_pos = config.paper.margin
cursor_y_pos = config.paper.margin


for filament in filaments:
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
    image.paste(type_text, (cursor_x_pos, cursor_y_pos))
    cursor_x_pos += config.label.type.width
    remaining_label_width -= config.label.type.width

    if filament.sub_type is not None:
        subtype_text = draw_text(
            filament.sub_type,
            config.label.subtype.font_size,
            config.label.height,
            config.label.subtype.width,
            (0, 0, 0),
            (255, 255, 255),
            config.label.subtype.margin_correction,
            90,
        )
        image.paste(subtype_text, (cursor_x_pos, cursor_y_pos))
        cursor_x_pos += config.label.subtype.width
        remaining_label_width -= config.label.subtype.width

    name_text = draw_text(
        filament.name,
        config.label.name.font_size,
        remaining_label_width,
        config.label.height,
        (255, 255, 255),
        (0, 0, 0),
        config.label.name.margin_correction,
        0,
    )
    image.paste(name_text, (cursor_x_pos, cursor_y_pos))
    cursor_x_pos += remaining_label_width


image.save(f"{filaments_file_path.stem}.png", dpi=(dpi, dpi))
