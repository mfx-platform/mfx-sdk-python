from enum import Enum


class EaFindingFoundBy(str, Enum):
    BUILD = "build"
    REVIEW = "review"
    RULES = "rules"
    SCAN = "scan"
    TRIAL = "trial"

    def __str__(self) -> str:
        return str(self.value)
