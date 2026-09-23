import sys
from typing import Self, Any

try:
    from pydantic import BaseModel, Field, model_validator
except ModuleNotFoundError as e:
    print(e)
    print("To install the module, run: 'make install'")
    sys.exit()


class InvalidFormatError(Exception):
    pass


class InvalidVariableError(Exception):
    pass


class InvalidValueFormatError(Exception):
    pass


class MissingVariableError(Exception):
    pass


class Values(BaseModel):
    width: int = Field(ge=1)
    height: int = Field(ge=1)
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool = Field(default=False)
    seed: int | None = Field(default=None)

    @model_validator(mode='after')
    def validator(self) -> Self:

        if self.entry[0] >= self.width or self.entry[1] >= self.height:
            raise ValueError("Entry must be inside the maze")

        if self.exit[0] >= self.width or self.exit[1] >= self.height:
            raise ValueError("Exit must be inside the maze")

        if self.entry[0] < 0 or self.entry[1] < 0:
            raise ValueError("Entry value can't be less than 0")

        if self.exit[0] < 0 or self.exit[1] < 0:
            raise ValueError("Exit value can't be less than 0")

        if self.entry[0] >= self.exit[0]:
            raise ValueError("Entry must be at the left of the exit")

        return self


def parse(config: str) -> Values:
    var = [
        "WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT", "SEED"
        ]
    dict_value = {}

    with open(config) as f:
        lines = f.readlines()

    for line in lines:
        line = line.rstrip("\n")
        key_value = line.rsplit("=")

        if line and line[0] != "#":

            if key_value[0] in var:

                if len(key_value) != 2:
                    raise InvalidFormatError(
                        f"Invalid key-value format: {line}"
                    )

                value: Any = None
                if (key_value[0] == "WIDTH" or key_value[0] == "HEIGHT"
                        or key_value[0] == "SEED"):
                    try:
                        value = int(key_value[1])
                    except ValueError:
                        raise InvalidValueFormatError(
                            f"{key_value[0]} must be int"
                            )

                elif key_value[0] == "ENTRY" or key_value[0] == "EXIT":
                    value = key_value[1].split(",")
                    if len(value) != 2:
                        raise InvalidFormatError(
                            "Invalid entry format: expected x,y"
                            )
                    try:
                        value[0] = int(value[0])
                        value[1] = int(value[1])
                    except ValueError:
                        raise InvalidValueFormatError(
                            f"{key_value[0]} coordinate must be int"
                            )
                    value = tuple(value)

                elif key_value[0] == "OUTPUT_FILE":
                    value = key_value[1]

                elif key_value[0] == "PERFECT":
                    if key_value[1] == "False":
                        value = False
                    elif key_value[1] == "True":
                        value = True
                    else:
                        raise InvalidValueFormatError(
                            f"{key_value[0]} must be bool"
                            )

            else:
                raise InvalidVariableError(
                    f"Invalid variable: {key_value[0]}"
                )

            dict_value.update({key_value[0].lower(): value})

    for key in var[:-2]:
        if not key.lower() in dict_value.keys():
            raise MissingVariableError(
                f"Missing required configuration variable: {key}"
                )

    values = Values(**dict_value)

    if values.width < 9 and values.height < 7:
        print("Warning: The maze is too small to display '42' logo")

    return values
