from enum import Enum


class TerminalHaModeType2Type1(str, Enum):
    HOT = "hot"
    WARM = "warm"

    def __str__(self) -> str:
        return str(self.value)
