from enum import Enum


class ListTradingAccountsStateItem(str, Enum):
    CONNECTED = "CONNECTED"
    CONNECTING = "CONNECTING"
    DEGRADED = "DEGRADED"
    FAILED = "FAILED"
    PAUSED = "PAUSED"
    PENDING = "PENDING"
    REAUTH_NEEDED = "REAUTH_NEEDED"
    RETIRED = "RETIRED"

    def __str__(self) -> str:
        return str(self.value)
