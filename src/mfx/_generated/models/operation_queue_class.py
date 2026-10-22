from enum import Enum


class OperationQueueClass(str, Enum):
    HEALING = "healing"
    OPERATOR = "operator"
    TENANT = "tenant"

    def __str__(self) -> str:
        return str(self.value)
