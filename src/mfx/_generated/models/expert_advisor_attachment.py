import datetime
from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    BinaryIO,
    Generator,
    Optional,
    TextIO,
    TypeVar,
    cast,
)
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.expert_advisor_attachment_state import ExpertAdvisorAttachmentState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ref import Ref


T = TypeVar("T", bound="ExpertAdvisorAttachment")


@_attrs_define
class ExpertAdvisorAttachment:
    """One terminal's attachment of a version: what the confirmation answers

    Attributes:
        terminal_id (UUID):
        expert_advisor (Ref): A resolved foreign key — enough to render and link, never a second fetch.
        state (ExpertAdvisorAttachmentState):
        since (datetime.datetime):
        symbol (str):
        timeframe (str):
    """

    terminal_id: UUID
    expert_advisor: "Ref"
    state: ExpertAdvisorAttachmentState
    since: datetime.datetime
    symbol: str
    timeframe: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.ref import Ref

        terminal_id = str(self.terminal_id)

        expert_advisor = self.expert_advisor.to_dict()

        state = self.state.value

        since = self.since.isoformat()

        symbol = self.symbol

        timeframe = self.timeframe

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "terminal_id": terminal_id,
                "expert_advisor": expert_advisor,
                "state": state,
                "since": since,
                "symbol": symbol,
                "timeframe": timeframe,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ref import Ref

        d = dict(src_dict)
        terminal_id = UUID(d.pop("terminal_id"))

        expert_advisor = Ref.from_dict(d.pop("expert_advisor"))

        state = ExpertAdvisorAttachmentState(d.pop("state"))

        since = isoparse(d.pop("since"))

        symbol = d.pop("symbol")

        timeframe = d.pop("timeframe")

        expert_advisor_attachment = cls(
            terminal_id=terminal_id,
            expert_advisor=expert_advisor,
            state=state,
            since=since,
            symbol=symbol,
            timeframe=timeframe,
        )

        expert_advisor_attachment.additional_properties = d
        return expert_advisor_attachment

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
