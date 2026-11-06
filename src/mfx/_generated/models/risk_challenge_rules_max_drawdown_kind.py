from enum import Enum


class RiskChallengeRulesMaxDrawdownKind(str, Enum):
    STATIC = "static"
    TRAILING = "trailing"

    def __str__(self) -> str:
        return str(self.value)
