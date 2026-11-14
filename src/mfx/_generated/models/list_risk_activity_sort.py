from enum import Enum


class ListRiskActivitySort(str, Enum):
    NEWEST = "newest"
    OLDEST = "oldest"
    UNRESOLVED_FIRST = "unresolved_first"

    def __str__(self) -> str:
        return str(self.value)
