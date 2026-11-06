from enum import Enum


class ListRiskAccountsCoverage(str, Enum):
    DEGRADED = "degraded"
    DISCONNECTED = "disconnected"
    HEALTHY = "healthy"
    NO_RULES = "no_rules"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
