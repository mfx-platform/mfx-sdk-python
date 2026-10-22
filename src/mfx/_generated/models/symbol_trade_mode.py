from enum import Enum


class SymbolTradeMode(str, Enum):
    CLOSEONLY = "closeonly"
    DISABLED = "disabled"
    FULL = "full"
    LONGONLY = "longonly"
    SHORTONLY = "shortonly"

    def __str__(self) -> str:
        return str(self.value)
