from enum import Enum


class TenantMaintenanceState(str, Enum):
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    IN_PROGRESS = "in_progress"
    SCHEDULED = "scheduled"

    def __str__(self) -> str:
        return str(self.value)
