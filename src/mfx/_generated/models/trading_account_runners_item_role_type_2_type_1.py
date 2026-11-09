from enum import Enum


class TradingAccountRunnersItemRoleType2Type1(str, Enum):
    STANDBY = "standby"
    WRITER = "writer"

    def __str__(self) -> str:
        return str(self.value)
