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

from ..models.account_profile_type_0_account_type import AccountProfileType0AccountType
from ..models.account_profile_type_0_margin_mode import AccountProfileType0MarginMode
from ..types import UNSET, Unset

T = TypeVar("T", bound="AccountProfileType0")


@_attrs_define
class AccountProfileType0:
    """
    Attributes:
        currency (Union[Unset, str]):
        currency_digits (Union[None, Unset, int]): How many decimals the account currency has (MT5
            ACCOUNT_CURRENCY_DIGITS): every money figure of this account carries exactly this many
        leverage (Union[Unset, int]):
        company (Union[Unset, str]):
        account_type (Union[Unset, AccountProfileType0AccountType]):
        margin_mode (Union[Unset, AccountProfileType0MarginMode]):
        trade_allowed (Union[Unset, bool]):
        expert_allowed (Union[Unset, bool]):
        max_sessions (Union[None, Unset, int]):
        observed_at (Union[Unset, datetime.datetime]):
    """

    currency: Union[Unset, str] = UNSET
    currency_digits: Union[None, Unset, int] = UNSET
    leverage: Union[Unset, int] = UNSET
    company: Union[Unset, str] = UNSET
    account_type: Union[Unset, AccountProfileType0AccountType] = UNSET
    margin_mode: Union[Unset, AccountProfileType0MarginMode] = UNSET
    trade_allowed: Union[Unset, bool] = UNSET
    expert_allowed: Union[Unset, bool] = UNSET
    max_sessions: Union[None, Unset, int] = UNSET
    observed_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        currency = self.currency

        currency_digits: Union[None, Unset, int]
        if isinstance(self.currency_digits, Unset):
            currency_digits = UNSET
        else:
            currency_digits = self.currency_digits

        leverage = self.leverage

        company = self.company

        account_type: Union[Unset, str] = UNSET
        if not isinstance(self.account_type, Unset):
            account_type = self.account_type.value

        margin_mode: Union[Unset, str] = UNSET
        if not isinstance(self.margin_mode, Unset):
            margin_mode = self.margin_mode.value

        trade_allowed = self.trade_allowed

        expert_allowed = self.expert_allowed

        max_sessions: Union[None, Unset, int]
        if isinstance(self.max_sessions, Unset):
            max_sessions = UNSET
        else:
            max_sessions = self.max_sessions

        observed_at: Union[Unset, str] = UNSET
        if not isinstance(self.observed_at, Unset):
            observed_at = self.observed_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if currency is not UNSET:
            field_dict["currency"] = currency
        if currency_digits is not UNSET:
            field_dict["currency_digits"] = currency_digits
        if leverage is not UNSET:
            field_dict["leverage"] = leverage
        if company is not UNSET:
            field_dict["company"] = company
        if account_type is not UNSET:
            field_dict["account_type"] = account_type
        if margin_mode is not UNSET:
            field_dict["margin_mode"] = margin_mode
        if trade_allowed is not UNSET:
            field_dict["trade_allowed"] = trade_allowed
        if expert_allowed is not UNSET:
            field_dict["expert_allowed"] = expert_allowed
        if max_sessions is not UNSET:
            field_dict["max_sessions"] = max_sessions
        if observed_at is not UNSET:
            field_dict["observed_at"] = observed_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        currency = d.pop("currency", UNSET)

        def _parse_currency_digits(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        currency_digits = _parse_currency_digits(d.pop("currency_digits", UNSET))

        leverage = d.pop("leverage", UNSET)

        company = d.pop("company", UNSET)

        _account_type = d.pop("account_type", UNSET)
        account_type: Union[Unset, AccountProfileType0AccountType]
        if isinstance(_account_type, Unset):
            account_type = UNSET
        else:
            account_type = AccountProfileType0AccountType(_account_type)

        _margin_mode = d.pop("margin_mode", UNSET)
        margin_mode: Union[Unset, AccountProfileType0MarginMode]
        if isinstance(_margin_mode, Unset):
            margin_mode = UNSET
        else:
            margin_mode = AccountProfileType0MarginMode(_margin_mode)

        trade_allowed = d.pop("trade_allowed", UNSET)

        expert_allowed = d.pop("expert_allowed", UNSET)

        def _parse_max_sessions(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        max_sessions = _parse_max_sessions(d.pop("max_sessions", UNSET))

        _observed_at = d.pop("observed_at", UNSET)
        observed_at: Union[Unset, datetime.datetime]
        if isinstance(_observed_at, Unset):
            observed_at = UNSET
        else:
            observed_at = isoparse(_observed_at)

        account_profile_type_0 = cls(
            currency=currency,
            currency_digits=currency_digits,
            leverage=leverage,
            company=company,
            account_type=account_type,
            margin_mode=margin_mode,
            trade_allowed=trade_allowed,
            expert_allowed=expert_allowed,
            max_sessions=max_sessions,
            observed_at=observed_at,
        )

        account_profile_type_0.additional_properties = d
        return account_profile_type_0

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
