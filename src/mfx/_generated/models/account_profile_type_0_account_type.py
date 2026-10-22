from enum import Enum


class AccountProfileType0AccountType(str, Enum):
    CONTEST = "contest"
    DEMO = "demo"
    LIVE = "live"

    def __str__(self) -> str:
        return str(self.value)
