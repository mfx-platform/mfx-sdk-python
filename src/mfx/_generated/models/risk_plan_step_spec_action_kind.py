from enum import Enum


class RiskPlanStepSpecActionKind(str, Enum):
    CLOSE_PART = "close_part"
    MOVE_STOP = "move_stop"
    SET_STOPS = "set_stops"
    TRAIL = "trail"

    def __str__(self) -> str:
        return str(self.value)
