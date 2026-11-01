from enum import Enum


class UsagePlan(str, Enum):
    ENTERPRISE = "enterprise"
    STANDARD = "standard"
    SYSTEM = "system"

    def __str__(self) -> str:
        return str(self.value)
