from enum import Enum


class TerminalStateChangedTo(str, Enum):
    ACTIVE = "ACTIVE"
    DRAINED = "DRAINED"
    DRAINING = "DRAINING"
    FAILED = "FAILED"
    LOGGING_IN = "LOGGING_IN"
    OFFLINE = "OFFLINE"
    PARKED = "PARKED"
    PROVISIONING = "PROVISIONING"
    REQUESTED = "REQUESTED"
    RETIRED = "RETIRED"

    def __str__(self) -> str:
        return str(self.value)
