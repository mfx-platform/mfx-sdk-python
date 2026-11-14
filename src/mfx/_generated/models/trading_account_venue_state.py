from enum import Enum


class TradingAccountVenueState(str, Enum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"
    SUSPENDED = "SUSPENDED"

    def __str__(self) -> str:
        return str(self.value)
