from argparse import ArgumentParser
from pathlib import Path

from renderer import render_filament_labels
from types_ import load_filaments_yaml, load_config, load_filaments_csv

parser = ArgumentParser()
parser.add_argument("filaments", type=Path)
parser.add_argument("-c", "--config", type=Path, default="config.yaml")

cli_args = parser.parse_args()

filaments_file_path: Path = cli_args.filaments

if filaments_file_path.suffix.lower() in (".yaml", ".yml"):
    filaments = load_filaments_yaml(filaments_file_path)
elif filaments_file_path.suffix.lower() == ".csv":
    filaments = load_filaments_csv(filaments_file_path)
else:
    print("Unhandled extension!")
    exit(1)

config = load_config(cli_args.config)

render_filament_labels(filaments, config, filaments_file_path.stem)
