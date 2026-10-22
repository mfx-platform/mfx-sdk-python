from enum import Enum


class TenantExpertAdvisorAnalysersItemAnalyser(str, Enum):
    BUILD = "build"
    REVIEW = "review"
    RULES = "rules"
    SCAN = "scan"

    def __str__(self) -> str:
        return str(self.value)
