from enum import Enum


class TenantTerminalReplicaRoleType3Type1(str, Enum):
    STANDBY = "standby"
    WRITER = "writer"

    def __str__(self) -> str:
        return str(self.value)
