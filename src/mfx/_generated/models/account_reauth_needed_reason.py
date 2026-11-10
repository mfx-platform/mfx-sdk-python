from enum import Enum


class AccountReauthNeededReason(str, Enum):
    EXPIRED = "expired"
    REVOKED = "revoked"
    TOKEN_INVALID = "token_invalid"

    def __str__(self) -> str:
        return str(self.value)
