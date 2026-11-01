from enum import Enum


class TerminalHaModeType1(str, Enum):
    HOT = "hot"
    WARM = "warm"

    def __str__(self) -> str:
        return str(self.value)
