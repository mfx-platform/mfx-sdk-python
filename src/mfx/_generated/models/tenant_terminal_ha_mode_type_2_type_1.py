from enum import Enum


class TenantTerminalHaModeType2Type1(str, Enum):
    HOT = "hot"
    WARM = "warm"

    def __str__(self) -> str:
        return str(self.value)
