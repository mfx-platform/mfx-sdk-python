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
    Union,
    cast,
)
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.tenant_expert_advisor_terminals_item_state import (
    TenantExpertAdvisorTerminalsItemState,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ea_trial import EaTrial


T = TypeVar("T", bound="TenantExpertAdvisorTerminalsItem")


@_attrs_define
class TenantExpertAdvisorTerminalsItem:
    """
    Attributes:
        terminal_id (UUID):
        state (TenantExpertAdvisorTerminalsItemState):
        since (datetime.datetime):
        symbol (str):
        timeframe (str): e.g. M1
        trial (Union['EaTrial', None, Unset]): The trial on this terminal, with its figures and verdict once judged;
            null while it is deploying, and absent from older answers
    """

    terminal_id: UUID
    state: TenantExpertAdvisorTerminalsItemState
    since: datetime.datetime
    symbol: str
    timeframe: str
    trial: Union["EaTrial", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.ea_trial import EaTrial

        terminal_id = str(self.terminal_id)

        state = self.state.value

        since = self.since.isoformat()

        symbol = self.symbol

        timeframe = self.timeframe

        trial: Union[None, Unset, dict[str, Any]]
        if isinstance(self.trial, Unset):
            trial = UNSET
        elif isinstance(self.trial, EaTrial):
            trial = self.trial.to_dict()
        else:
            trial = self.trial

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "terminal_id": terminal_id,
                "state": state,
                "since": since,
                "symbol": symbol,
                "timeframe": timeframe,
            }
        )
        if trial is not UNSET:
            field_dict["trial"] = trial

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ea_trial import EaTrial

        d = dict(src_dict)
        terminal_id = UUID(d.pop("terminal_id"))

        state = TenantExpertAdvisorTerminalsItemState(d.pop("state"))

        since = isoparse(d.pop("since"))

        symbol = d.pop("symbol")

        timeframe = d.pop("timeframe")

        def _parse_trial(data: object) -> Union["EaTrial", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                trial_type_0 = EaTrial.from_dict(data)

                return trial_type_0
            except:  # noqa: E722
                pass
            return cast(Union["EaTrial", None, Unset], data)

        trial = _parse_trial(d.pop("trial", UNSET))

        tenant_expert_advisor_terminals_item = cls(
            terminal_id=terminal_id,
            state=state,
            since=since,
            symbol=symbol,
            timeframe=timeframe,
            trial=trial,
        )

        tenant_expert_advisor_terminals_item.additional_properties = d
        return tenant_expert_advisor_terminals_item

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
