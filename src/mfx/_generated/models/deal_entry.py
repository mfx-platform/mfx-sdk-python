from enum import Enum


class DealEntry(str, Enum):
    IN = "in"
    INOUT = "inout"
    OUT = "out"

    def __str__(self) -> str:
        return str(self.value)
