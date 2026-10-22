from enum import Enum


class EaTrialFigureGradeType1(str, Enum):
    AMBER = "amber"
    GREEN = "green"
    RED = "red"

    def __str__(self) -> str:
        return str(self.value)
