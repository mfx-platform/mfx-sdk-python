from enum import Enum


class CtraderGrantCreateScope(str, Enum):
    ACCOUNTS = "accounts"
    TRADING = "trading"

    def __str__(self) -> str:
        return str(self.value)
