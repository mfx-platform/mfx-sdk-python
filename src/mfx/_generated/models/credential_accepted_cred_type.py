from enum import Enum


class CredentialAcceptedCredType(str, Enum):
    INVESTOR = "investor"
    MASTER = "master"

    def __str__(self) -> str:
        return str(self.value)
