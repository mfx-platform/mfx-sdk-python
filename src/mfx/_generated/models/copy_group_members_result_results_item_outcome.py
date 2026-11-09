from enum import Enum


class CopyGroupMembersResultResultsItemOutcome(str, Enum):
    DONE = "done"
    REFUSED = "refused"
    UNCHANGED = "unchanged"

    def __str__(self) -> str:
        return str(self.value)
