from enum import Enum


class CtraderGrantState(str, Enum):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    PENDING = "PENDING"
    REVOKED = "REVOKED"

    def __str__(self) -> str:
        return str(self.value)
