from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, Optional, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.trade_session_day import TradeSessionDay
from ..types import UNSET, Unset

T = TypeVar("T", bound="TradeSession")


@_attrs_define
class TradeSession:
    """One trade session in BROKER time, as MT5 reports it.

    Attributes:
        day (TradeSessionDay):
        from_ (str):
        to (str): 24:00 means end of day
    """

    day: TradeSessionDay
    from_: str
    to: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        day = self.day.value

        from_ = self.from_

        to = self.to

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "day": day,
                "from": from_,
                "to": to,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        day = TradeSessionDay(d.pop("day"))

        from_ = d.pop("from")

        to = d.pop("to")

        trade_session = cls(
            day=day,
            from_=from_,
            to=to,
        )

        trade_session.additional_properties = d
        return trade_session

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
