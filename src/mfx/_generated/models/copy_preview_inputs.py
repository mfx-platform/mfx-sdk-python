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

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="CopyPreviewInputs")


@_attrs_define
class CopyPreviewInputs:
    """The figures the rows were worked from

    Attributes:
        leader_currency (Union[None, str]):
        follower_currency (Union[None, str]):
        rate (Union[None, str]): Leader currency to follower currency; null when the currencies are the same or no rate
            is current
        leader_balance (Union[None, str]):
        leader_equity (Union[None, str]):
        follower_balance (Union[None, str]):
        follower_equity (Union[None, str]):
        read_at (Union[None, datetime.datetime]):
    """

    leader_currency: Union[None, str]
    follower_currency: Union[None, str]
    rate: Union[None, str]
    leader_balance: Union[None, str]
    leader_equity: Union[None, str]
    follower_balance: Union[None, str]
    follower_equity: Union[None, str]
    read_at: Union[None, datetime.datetime]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        leader_currency: Union[None, str]
        leader_currency = self.leader_currency

        follower_currency: Union[None, str]
        follower_currency = self.follower_currency

        rate: Union[None, str]
        rate = self.rate

        leader_balance: Union[None, str]
        leader_balance = self.leader_balance

        leader_equity: Union[None, str]
        leader_equity = self.leader_equity

        follower_balance: Union[None, str]
        follower_balance = self.follower_balance

        follower_equity: Union[None, str]
        follower_equity = self.follower_equity

        read_at: Union[None, str]
        if isinstance(self.read_at, datetime.datetime):
            read_at = self.read_at.isoformat()
        else:
            read_at = self.read_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "leader_currency": leader_currency,
                "follower_currency": follower_currency,
                "rate": rate,
                "leader_balance": leader_balance,
                "leader_equity": leader_equity,
                "follower_balance": follower_balance,
                "follower_equity": follower_equity,
                "read_at": read_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_leader_currency(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        leader_currency = _parse_leader_currency(d.pop("leader_currency"))

        def _parse_follower_currency(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        follower_currency = _parse_follower_currency(d.pop("follower_currency"))

        def _parse_rate(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        rate = _parse_rate(d.pop("rate"))

        def _parse_leader_balance(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        leader_balance = _parse_leader_balance(d.pop("leader_balance"))

        def _parse_leader_equity(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        leader_equity = _parse_leader_equity(d.pop("leader_equity"))

        def _parse_follower_balance(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        follower_balance = _parse_follower_balance(d.pop("follower_balance"))

        def _parse_follower_equity(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        follower_equity = _parse_follower_equity(d.pop("follower_equity"))

        def _parse_read_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                read_at_type_0 = isoparse(data)

                return read_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        read_at = _parse_read_at(d.pop("read_at"))

        copy_preview_inputs = cls(
            leader_currency=leader_currency,
            follower_currency=follower_currency,
            rate=rate,
            leader_balance=leader_balance,
            leader_equity=leader_equity,
            follower_balance=follower_balance,
            follower_equity=follower_equity,
            read_at=read_at,
        )

        copy_preview_inputs.additional_properties = d
        return copy_preview_inputs

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
