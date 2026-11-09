from enum import Enum


class TradingAccountVenue(str, Enum):
    CTRADER = "ctrader"
    MT5 = "mt5"

    def __str__(self) -> str:
        return str(self.value)
