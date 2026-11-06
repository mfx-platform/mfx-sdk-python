from enum import Enum


class RiskPlanStepSpecTriggerKind(str, Enum):
    AFTER_STEP = "after_step"
    FILLED = "filled"
    MONEY = "money"
    PCT = "pct"
    PRICE = "price"
    R = "r"

    def __str__(self) -> str:
        return str(self.value)
