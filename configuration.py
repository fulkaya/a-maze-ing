from pydantic import BaseModel, Field, model_validator
from typing import Self


class InvalidFormatError(Exception):
    pass


class InvalidVariableError(Exception):
    pass


class Values(BaseModel):
    width: int = Field(ge=1)
    height: int = Field(ge=1)
    entry: tuple[int, int]
    exit: tuple[int, int]
    perfect: bool = Field(default=False)
    seed: bool = Field(default=False)
    output_file: str

    @model_validator(mode='after')
    def validator(self) -> Self:

        for e in self.entry:
            if e < 0:
                raise ValueError("Entry value can't be less than 0")

        for e in self.exit:
            if e < 0:
                raise ValueError("Exit value can't be less than 0")

        return self


def parse(config):
    dict_value = {"width": "", "height": "", "entry": "",
                  "exit": "", "output_file": "",
                  "perfect": "False", "seed": "False"}

    with open(config) as f:
        lines = f.readlines()

    for line in lines:
        line = line.rstrip("\n")
        key_value = line.rsplit("=")

        if len(key_value) != 2:
            raise InvalidFormatError(
                f"Invalid key-value format: {line}"
            )

        if key_value[0].lower() not in dict_value.keys():
            raise InvalidVariableError(
                f"Invalid variable: {key_value[0]}"
            )

        dict_value[(key_value[0].lower())] = key_value[1]

    dict_value["entry"] = tuple(dict_value["entry"].split(","))
    dict_value["exit"] = tuple(dict_value["exit"].split(","))
    if len(dict_value["entry"]) != 2 or len(dict_value["exit"]) != 2:
        raise InvalidFormatError(
                        "Invalid value format: expected x,y")

    values = Values(**dict_value)

    return values
