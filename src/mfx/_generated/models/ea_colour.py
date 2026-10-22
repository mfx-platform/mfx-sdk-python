from enum import Enum


class EaColour(str, Enum):
    AMBER = "amber"
    GREEN = "green"
    GREY = "grey"
    RED = "red"

    def __str__(self) -> str:
        return str(self.value)
