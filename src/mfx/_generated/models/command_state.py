from enum import Enum


class CommandState(str, Enum):
    ACCEPTED = "ACCEPTED"
    DELIVERED = "DELIVERED"
    ENQUEUED = "ENQUEUED"
    EXECUTING = "EXECUTING"
    EXPIRED = "EXPIRED"
    FAILED = "FAILED"
    REJECTED = "REJECTED"
    SUCCEEDED = "SUCCEEDED"
    UNKNOWN = "UNKNOWN"

    def __str__(self) -> str:
        return str(self.value)
