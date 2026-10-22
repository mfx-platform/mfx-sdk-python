from enum import Enum


class OperationAcceptedState(str, Enum):
    ACCEPTED = "ACCEPTED"
    CANCELLED = "CANCELLED"
    CLOSING = "CLOSING"
    EXPIRED = "EXPIRED"
    FAILED = "FAILED"
    FORCED_STOP = "FORCED_STOP"
    NOT_STARTED = "NOT_STARTED"
    QUEUED = "QUEUED"
    RELAUNCHING = "RELAUNCHING"
    SUCCEEDED = "SUCCEEDED"
    SUPERSEDED = "SUPERSEDED"

    def __str__(self) -> str:
        return str(self.value)
