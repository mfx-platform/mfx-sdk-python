from enum import Enum


class TenantTerminalHaFallbackState(str, Enum):
    OFF = "off"
    READY = "ready"
    REPAIRING = "repairing"
    STARTING = "starting"
    WAITING_FOR_CAPACITY = "waiting_for_capacity"

    def __str__(self) -> str:
        return str(self.value)
