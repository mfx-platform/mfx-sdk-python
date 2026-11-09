from enum import Enum


class BulkActionState(str, Enum):
    CANCELLED = "CANCELLED"
    DONE = "DONE"
    PARTIAL = "PARTIAL"
    RUNNING = "RUNNING"

    def __str__(self) -> str:
        return str(self.value)
