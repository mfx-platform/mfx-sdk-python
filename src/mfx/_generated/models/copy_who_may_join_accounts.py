from enum import Enum


class CopyWhoMayJoinAccounts(str, Enum):
    ANY = "any"
    LISTED = "listed"

    def __str__(self) -> str:
        return str(self.value)
