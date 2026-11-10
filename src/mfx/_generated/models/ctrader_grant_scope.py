from enum import Enum


class CtraderGrantScope(str, Enum):
    ACCOUNTS = "accounts"
    TRADING = "trading"

    def __str__(self) -> str:
        return str(self.value)
