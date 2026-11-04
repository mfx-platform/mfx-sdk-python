from enum import Enum


class MaintenanceWindowChangedChange(str, Enum):
    ANNOUNCED = "announced"
    CANCELLED = "cancelled"
    ENDED = "ended"
    ETA_MOVED = "eta_moved"
    MESSAGE_CHANGED = "message_changed"
    STARTED = "started"

    def __str__(self) -> str:
        return str(self.value)
