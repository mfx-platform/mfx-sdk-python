from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, Optional, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CopyExternalOpenAccountType0")


@_attrs_define
class CopyExternalOpenAccountType0:
    """The source's own account figures where it has them; kept with the signal, read by no follower

    Attributes:
        currency (str):
        balance (str): A decimal as a string, never a JSON number
        equity (str): A decimal as a string, never a JSON number
    """

    currency: str
    balance: str
    equity: str

    def to_dict(self) -> dict[str, Any]:
        currency = self.currency

        balance = self.balance

        equity = self.equity

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "currency": currency,
                "balance": balance,
                "equity": equity,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        currency = d.pop("currency")

        balance = d.pop("balance")

        equity = d.pop("equity")

        copy_external_open_account_type_0 = cls(
            currency=currency,
            balance=balance,
            equity=equity,
        )

        return copy_external_open_account_type_0
