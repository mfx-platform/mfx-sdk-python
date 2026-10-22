from enum import Enum


class UsageBudgetSource(str, Enum):
    CONFIGURED = "configured"
    COUNTED = "counted"
    UNCONFIGURED = "unconfigured"

    def __str__(self) -> str:
        return str(self.value)
