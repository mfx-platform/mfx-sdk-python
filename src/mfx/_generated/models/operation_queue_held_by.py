from enum import Enum


class OperationQueueHeldBy(str, Enum):
    COOLDOWN = "cooldown"
    FARM_CAPACITY = "farm_capacity"
    TENANT_CONCURRENCY = "tenant_concurrency"
    TENANT_RATE = "tenant_rate"

    def __str__(self) -> str:
        return str(self.value)
