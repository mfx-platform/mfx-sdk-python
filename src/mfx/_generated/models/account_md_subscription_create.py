from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, Optional, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AccountMdSubscriptionCreate")


@_attrs_define
class AccountMdSubscriptionCreate:
    """
    Attributes:
        symbol (str): As `GET /accounts/{id}/symbols` lists it
    """

    symbol: str

    def to_dict(self) -> dict[str, Any]:
        symbol = self.symbol

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "symbol": symbol,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        symbol = d.pop("symbol")

        account_md_subscription_create = cls(
            symbol=symbol,
        )

        return account_md_subscription_create
