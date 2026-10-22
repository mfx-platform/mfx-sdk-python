from enum import Enum


class EaTrialFigureGradeType2Type1(str, Enum):
    AMBER = "amber"
    GREEN = "green"
    RED = "red"

    def __str__(self) -> str:
        return str(self.value)
