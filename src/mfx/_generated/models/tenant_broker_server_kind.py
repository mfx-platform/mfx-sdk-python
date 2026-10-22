from enum import Enum


class TenantBrokerServerKind(str, Enum):
    DEMO = "demo"
    LIVE = "live"

    def __str__(self) -> str:
        return str(self.value)
