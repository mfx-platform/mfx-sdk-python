from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    BinaryIO,
    Generator,
    Optional,
    TextIO,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TerminalRestart")


@_attrs_define
class TerminalRestart:
    """
    Attributes:
        reason (str): Why; written to the audit log and sent to the cell
        queue (Union[Unset, bool]): When the ask is valid and refused only because the platform is busy (rule 2
            cooldown, 4 tenant rate, 5 tenant concurrency, 6 farm capacity), hold it and start it when it can, instead of
            answering 429. The answer is then 202 with `state: QUEUED` and where it waits. Without it the 429 stays, as
            before. A hold that could not end before the queue's deadline is refused at once either way Default: False.
        confirm_open_positions (Union[Unset, bool]): Rule 3: required true when the terminal has open positions, or
            while the platform cannot yet tell (until the account's first snapshot has arrived), and only while the
            platform's open-position confirmation setting is on (it is off unless an operator turns it on). Off, it is not
            needed Default: False.
    """

    reason: str
    queue: Union[Unset, bool] = False
    confirm_open_positions: Union[Unset, bool] = False

    def to_dict(self) -> dict[str, Any]:
        reason = self.reason

        queue = self.queue

        confirm_open_positions = self.confirm_open_positions

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "reason": reason,
            }
        )
        if queue is not UNSET:
            field_dict["queue"] = queue
        if confirm_open_positions is not UNSET:
            field_dict["confirm_open_positions"] = confirm_open_positions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        reason = d.pop("reason")

        queue = d.pop("queue", UNSET)

        confirm_open_positions = d.pop("confirm_open_positions", UNSET)

        terminal_restart = cls(
            reason=reason,
            queue=queue,
            confirm_open_positions=confirm_open_positions,
        )

        return terminal_restart
