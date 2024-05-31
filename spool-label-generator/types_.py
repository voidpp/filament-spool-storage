from pathlib import Path

from pydantic import BaseModel, TypeAdapter
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from yaml import safe_load

from funcs import mm


class FilamentTypeDescriptor(BaseModel):
    label: str
    color: tuple[int, int, int]


class Filament(BaseModel):
    type: str
    name: str
    sub_type: str | None = None


px = Annotated[int, BeforeValidator(mm)]


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


def load_filaments(file: Path) -> list[Filament]:
    ta = TypeAdapter(list[Filament])
    return ta.validate_python(safe_load(file.read_text()))


def load_config(file: Path) -> Config:
    return Config(**safe_load(file.read_text()))
