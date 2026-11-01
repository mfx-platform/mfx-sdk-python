from enum import Enum


class UsageLimitSource(str, Enum):
    KEY_OVERRIDE = "key_override"
    PLAN = "plan"
    TENANT_OVERRIDE = "tenant_override"

    def __str__(self) -> str:
        return str(self.value)
