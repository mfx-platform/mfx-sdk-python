from enum import Enum


class RiskPolicyAccountsItemState(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"

    def __str__(self) -> str:
        return str(self.value)
