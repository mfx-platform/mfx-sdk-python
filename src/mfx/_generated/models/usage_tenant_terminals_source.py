from enum import Enum


class UsageTenantTerminalsSource(str, Enum):
    PLATFORM_DEFAULT = "platform_default"
    TENANT_OVERRIDE = "tenant_override"

    def __str__(self) -> str:
        return str(self.value)
