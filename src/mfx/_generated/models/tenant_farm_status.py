from enum import Enum


class TenantFarmStatus(str, Enum):
    ACTIVE = "active"
    DISABLED = "disabled"
    DRAFT = "draft"
    DRAINING = "draining"
    PROVISIONING = "provisioning"
    RETIRED = "retired"
    SUSPENDED = "suspended"

    def __str__(self) -> str:
        return str(self.value)
