from enum import Enum


class ListRiskPoliciesSort(str, Enum):
    NEWEST = "newest"
    OLDEST = "oldest"

    def __str__(self) -> str:
        return str(self.value)
