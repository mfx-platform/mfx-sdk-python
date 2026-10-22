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
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.expert_advisor_attach_timeframe import ExpertAdvisorAttachTimeframe
from ..types import UNSET, Unset

T = TypeVar("T", bound="ExpertAdvisorAttach")


@_attrs_define
class ExpertAdvisorAttach:
    """Attach an approved version to a terminal. A governed operation of kind `attach`: the terminal is relaunched with the
    expert loaded and trading by experts off, and the operation succeeds when the terminal produces again, which is when
    the trial starts.

        Attributes:
            expert_advisor_id (UUID): The version; it must be `approved` and built for the MetaTrader build the terminal's
                farm runs
            symbol (str): The chart's symbol, in the broker's own name; one the terminal's server lists
            timeframe (ExpertAdvisorAttachTimeframe): The chart's timeframe
            reason (str): Why; written to the audit log
            queue (Union[Unset, bool]): As on TerminalRestart Default: False.
            confirm_open_positions (Union[Unset, bool]): As on TerminalRestart Default: False.
    """

    expert_advisor_id: UUID
    symbol: str
    timeframe: ExpertAdvisorAttachTimeframe
    reason: str
    queue: Union[Unset, bool] = False
    confirm_open_positions: Union[Unset, bool] = False

    def to_dict(self) -> dict[str, Any]:
        expert_advisor_id = str(self.expert_advisor_id)

        symbol = self.symbol

        timeframe = self.timeframe.value

        reason = self.reason

        queue = self.queue

        confirm_open_positions = self.confirm_open_positions

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "expert_advisor_id": expert_advisor_id,
                "symbol": symbol,
                "timeframe": timeframe,
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
        expert_advisor_id = UUID(d.pop("expert_advisor_id"))

        symbol = d.pop("symbol")

        timeframe = ExpertAdvisorAttachTimeframe(d.pop("timeframe"))

        reason = d.pop("reason")

        queue = d.pop("queue", UNSET)

        confirm_open_positions = d.pop("confirm_open_positions", UNSET)

        expert_advisor_attach = cls(
            expert_advisor_id=expert_advisor_id,
            symbol=symbol,
            timeframe=timeframe,
            reason=reason,
            queue=queue,
            confirm_open_positions=confirm_open_positions,
        )

        return expert_advisor_attach
