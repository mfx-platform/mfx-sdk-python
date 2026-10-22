from enum import Enum


class CredentialSubmissionCredType(str, Enum):
    INVESTOR = "investor"
    MASTER = "master"

    def __str__(self) -> str:
        return str(self.value)
