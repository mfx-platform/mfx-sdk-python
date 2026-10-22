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

T = TypeVar("T", bound="AccountSnapshotType0")


@_attrs_define
class AccountSnapshotType0:
    """
    Attributes:
        ts (Union[Unset, datetime.datetime]):
        balance (Union[Unset, str]): Decimal as a string, in the account currency
        equity (Union[Unset, str]):
        margin (Union[Unset, str]):
        margin_free (Union[Unset, str]):
        margin_level (Union[None, Unset, str]): Null with no open positions
        credit (Union[None, Unset, str]): The broker's credit on the account (MT5 ACCOUNT_CREDIT), in the account
            currency; part of equity, not of balance. Null from a cell that does not send it
        open_positions_count (Union[Unset, int]):
    """

    ts: Union[Unset, datetime.datetime] = UNSET
    balance: Union[Unset, str] = UNSET
    equity: Union[Unset, str] = UNSET
    margin: Union[Unset, str] = UNSET
    margin_free: Union[Unset, str] = UNSET
    margin_level: Union[None, Unset, str] = UNSET
    credit: Union[None, Unset, str] = UNSET
    open_positions_count: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ts: Union[Unset, str] = UNSET
        if not isinstance(self.ts, Unset):
            ts = self.ts.isoformat()

        balance = self.balance

        equity = self.equity

        margin = self.margin

        margin_free = self.margin_free

        margin_level: Union[None, Unset, str]
        if isinstance(self.margin_level, Unset):
            margin_level = UNSET
        else:
            margin_level = self.margin_level

        credit: Union[None, Unset, str]
        if isinstance(self.credit, Unset):
            credit = UNSET
        else:
            credit = self.credit

        open_positions_count = self.open_positions_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if ts is not UNSET:
            field_dict["ts"] = ts
        if balance is not UNSET:
            field_dict["balance"] = balance
        if equity is not UNSET:
            field_dict["equity"] = equity
        if margin is not UNSET:
            field_dict["margin"] = margin
        if margin_free is not UNSET:
            field_dict["margin_free"] = margin_free
        if margin_level is not UNSET:
            field_dict["margin_level"] = margin_level
        if credit is not UNSET:
            field_dict["credit"] = credit
        if open_positions_count is not UNSET:
            field_dict["open_positions_count"] = open_positions_count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _ts = d.pop("ts", UNSET)
        ts: Union[Unset, datetime.datetime]
        if isinstance(_ts, Unset):
            ts = UNSET
        else:
            ts = isoparse(_ts)

        balance = d.pop("balance", UNSET)

        equity = d.pop("equity", UNSET)

        margin = d.pop("margin", UNSET)

        margin_free = d.pop("margin_free", UNSET)

        def _parse_margin_level(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        margin_level = _parse_margin_level(d.pop("margin_level", UNSET))

        def _parse_credit(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        credit = _parse_credit(d.pop("credit", UNSET))

        open_positions_count = d.pop("open_positions_count", UNSET)

        account_snapshot_type_0 = cls(
            ts=ts,
            balance=balance,
            equity=equity,
            margin=margin,
            margin_free=margin_free,
            margin_level=margin_level,
            credit=credit,
            open_positions_count=open_positions_count,
        )

        account_snapshot_type_0.additional_properties = d
        return account_snapshot_type_0

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
