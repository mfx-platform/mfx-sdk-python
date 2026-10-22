from enum import Enum


class TenantBrokerStatus(str, Enum):
    ACTIVE = "active"
    PENDING = "pending"
    RETIRED = "retired"
    SUSPENDED = "suspended"

    def __str__(self) -> str:
        return str(self.value)
