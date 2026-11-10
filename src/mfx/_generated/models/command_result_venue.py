from enum import Enum


class CommandResultVenue(str, Enum):
    CTRADER = "ctrader"
    MT5 = "mt5"

    def __str__(self) -> str:
        return str(self.value)
