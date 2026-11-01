from enum import Enum


class TerminalHaSwitchedReason(str, Enum):
    BROKER_LOST = "broker_lost"
    OPERATOR = "operator"
    ORDER = "order"
    PROCESS_GONE = "process_gone"
    TERMINAL_FAILED = "terminal_failed"
    UNRESPONSIVE = "unresponsive"

    def __str__(self) -> str:
        return str(self.value)
