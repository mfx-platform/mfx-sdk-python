from enum import Enum


class CandleListSource(str, Enum):
    STORE = "store"
    STORETERMINAL = "store+terminal"
    TERMINAL = "terminal"

    def __str__(self) -> str:
        return str(self.value)
