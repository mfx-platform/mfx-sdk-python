from enum import Enum


class UsageRowMetric(str, Enum):
    COMMANDS = "commands"
    MD_MSGS = "md_msgs"
    TERMINAL_HOURS = "terminal_hours"
    WS_MINUTES = "ws_minutes"

    def __str__(self) -> str:
        return str(self.value)
