from enum import Enum


class CtraderGrantEnvironment(str, Enum):
    DEMO = "demo"
    LIVE = "live"

    def __str__(self) -> str:
        return str(self.value)
