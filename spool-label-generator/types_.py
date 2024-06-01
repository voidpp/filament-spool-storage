import csv
from pathlib import Path

from pydantic import BaseModel, TypeAdapter
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from yaml import safe_load

from contants import dpi, inch_mm


class FilamentTypeDescriptor(BaseModel):
    label: str
    color: tuple[int, int, int]


class Filament(BaseModel):
    type: str
    name: str
    sub_type: str | None = None

    def render_name(self):
        yield self.name


class FilamentManufacturer(Filament):
    manufacturer_name: str
    manufacturer_name_short: str | None = None

    def render_name(self):
        yield from self._generate_name_variations(f"{self.name} ({self.manufacturer_name})")

        if self.manufacturer_name_short:
            yield from self._generate_name_variations(f"{self.name} ({self.manufacturer_name_short})")

    def _generate_name_variations(self, full_name: str):
        words = full_name.split(" ")
        for idx in range(len(words) - 1):
            yield " ".join(words[: -(idx + 1)]) + "\n" + " ".join(words[-(idx + 1) :])


def mm_to_px(value: float) -> int:
    return int(round(value * dpi / inch_mm))


px = Annotated[int, BeforeValidator(mm_to_px)]


class PaperConfig(BaseModel):
    width: px
    height: px
    margin: px


class LabelSectionConfig(BaseModel):
    font_size: px
    margin_correction: px


class LabelTagSectionConfig(LabelSectionConfig):
    width: px


class LabelConfig(BaseModel):
    width: px
    height: px
    type: LabelTagSectionConfig
    subtype: LabelTagSectionConfig
    name: LabelSectionConfig


class Config(BaseModel):
    types: dict[str, FilamentTypeDescriptor]
    paper: PaperConfig
    label: LabelConfig


def load_filaments_yaml(file: Path) -> list[Filament]:
    ta = TypeAdapter(list[Filament])
    return ta.validate_python(safe_load(file.read_text()))


def load_config(file: Path) -> Config:
    return Config(**safe_load(file.read_text()))


def load_filaments_csv(file: Path) -> list[FilamentManufacturer]:
    filaments: list[FilamentManufacturer] = []

    with file.open() as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            filaments.append(
                FilamentManufacturer(
                    manufacturer_name=row[1], manufacturer_name_short=row[2], type=row[3], sub_type=row[4], name=row[5]
                )
            )

    return filaments
