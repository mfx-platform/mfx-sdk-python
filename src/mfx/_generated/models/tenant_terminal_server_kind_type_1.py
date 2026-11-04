from enum import Enum


class TenantTerminalServerKindType1(str, Enum):
    DEMO = "demo"
    LIVE = "live"

    def __str__(self) -> str:
        return str(self.value)
