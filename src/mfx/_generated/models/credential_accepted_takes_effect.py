from enum import Enum


class CredentialAcceptedTakesEffect(str, Enum):
    FIRST_LOGIN = "first_login"
    NEXT_LOGIN = "next_login"
    RESTART = "restart"
    RETRY_LOGIN = "retry_login"

    def __str__(self) -> str:
        return str(self.value)
