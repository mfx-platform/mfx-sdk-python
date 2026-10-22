from enum import Enum


class AccountProfileChangedAccountType(str, Enum):
    CONTEST = "contest"
    DEMO = "demo"
    LIVE = "live"

    def __str__(self) -> str:
        return str(self.value)
