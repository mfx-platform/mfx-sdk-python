from enum import Enum


class ListRiskPlansSort(str, Enum):
    NEWEST = "newest"
    OLDEST = "oldest"

    def __str__(self) -> str:
        return str(self.value)
