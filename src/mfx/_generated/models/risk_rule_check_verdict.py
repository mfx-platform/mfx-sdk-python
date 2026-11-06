from enum import Enum


class RiskRuleCheckVerdict(str, Enum):
    NOT_APPLICABLE = "not_applicable"
    PASS = "pass"
    REFUSE = "refuse"

    def __str__(self) -> str:
        return str(self.value)
