from enum import Enum


class TenantTerminalOfflineReasonType1(str, Enum):
    NO_HEARTBEAT = "no_heartbeat"
    POWER_OFF = "power_off"
    VM_MISSING = "vm_missing"

    def __str__(self) -> str:
        return str(self.value)
