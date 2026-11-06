from enum import Enum


class ListRiskPoliciesState(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"

    def __str__(self) -> str:
        return str(self.value)
