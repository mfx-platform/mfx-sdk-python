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

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CtraderAccountsChoice")


@_attrs_define
class CtraderAccountsChoice:
    """
    Attributes:
        ctid_trader_account_ids (list[str]): The accounts of this grant to connect to MFX Hub, by cTrader's id
    """

    ctid_trader_account_ids: list[str]

    def to_dict(self) -> dict[str, Any]:
        ctid_trader_account_ids = self.ctid_trader_account_ids

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "ctid_trader_account_ids": ctid_trader_account_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ctid_trader_account_ids = cast(list[str], d.pop("ctid_trader_account_ids"))

        ctrader_accounts_choice = cls(
            ctid_trader_account_ids=ctid_trader_account_ids,
        )

        return ctrader_accounts_choice
