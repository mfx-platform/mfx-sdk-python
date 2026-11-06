from enum import Enum


class RiskDrawdownKind(str, Enum):
    STATIC = "static"
    TRAILING = "trailing"

    def __str__(self) -> str:
        return str(self.value)
