from enum import Enum


class TenantMaintenanceConsole(str, Enum):
    NORMAL = "normal"
    READ_ONLY = "read_only"
    UNAVAILABLE = "unavailable"

    def __str__(self) -> str:
        return str(self.value)
