from enum import Enum


class EaFindingColour(str, Enum):
    AMBER = "amber"
    GREY = "grey"
    NOTE = "note"
    RED = "red"

    def __str__(self) -> str:
        return str(self.value)
