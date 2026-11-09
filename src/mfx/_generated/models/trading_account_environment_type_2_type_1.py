from enum import Enum


class TradingAccountEnvironmentType2Type1(str, Enum):
    DEMO = "demo"
    LIVE = "live"

    def __str__(self) -> str:
        return str(self.value)
