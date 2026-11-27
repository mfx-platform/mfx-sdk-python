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

from ..models.plan_change_summary_state import PlanChangeSummaryState
from ..types import UNSET, Unset

T = TypeVar("T", bound="PlanChangeSummary")


@_attrs_define
class PlanChangeSummary:
    """A move from one plan to another, as the customer sees it

    Attributes:
        id (UUID):
        from_ (str): The plan now: standard or enterprise
        to (str): The plan after acceptance: standard or enterprise (developer when it launches)
        state (PlanChangeSummaryState):
        requested_at (datetime.datetime):
        until (Union[None, datetime.datetime]): When an awaiting change lapses if nobody accepts it; null once decided
        requested_by_operator (bool): MFX Hub asked for the change (true) or the organisation did (false)
    """

    id: UUID
    from_: str
    to: str
    state: PlanChangeSummaryState
    requested_at: datetime.datetime
    until: Union[None, datetime.datetime]
    requested_by_operator: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        from_ = self.from_

        to = self.to

        state = self.state.value

        requested_at = self.requested_at.isoformat()

        until: Union[None, str]
        if isinstance(self.until, datetime.datetime):
            until = self.until.isoformat()
        else:
            until = self.until

        requested_by_operator = self.requested_by_operator

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "from": from_,
                "to": to,
                "state": state,
                "requested_at": requested_at,
                "until": until,
                "requested_by_operator": requested_by_operator,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        from_ = d.pop("from")

        to = d.pop("to")

        state = PlanChangeSummaryState._read(d.pop("state"))

        requested_at = isoparse(d.pop("requested_at"))

        def _parse_until(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                until_type_0 = isoparse(data)

                return until_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        until = _parse_until(d.pop("until"))

        requested_by_operator = d.pop("requested_by_operator")

        plan_change_summary = cls(
            id=id,
            from_=from_,
            to=to,
            state=state,
            requested_at=requested_at,
            until=until,
            requested_by_operator=requested_by_operator,
        )

        plan_change_summary.additional_properties = d
        return plan_change_summary

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
