from enum import Enum


class CopyLeaderSource(str, Enum):
    ACCOUNT = "account"
    EXTERNAL = "external"

    def __str__(self) -> str:
        return str(self.value)
