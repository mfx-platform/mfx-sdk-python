from enum import Enum


class TenantMaintenanceTerminalState(str, Enum):
    ATTENTION = "attention"
    BACK = "back"
    MIGRATING = "migrating"
    WAITING = "waiting"

    def __str__(self) -> str:
        return str(self.value)
