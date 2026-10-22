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

from ..models.account_profile_changed_account_type import (
    AccountProfileChangedAccountType,
)
from ..models.account_profile_changed_expert_allowed import (
    AccountProfileChangedExpertAllowed,
)
from ..models.account_profile_changed_margin_mode import AccountProfileChangedMarginMode
from ..models.account_profile_changed_trade_allowed import (
    AccountProfileChangedTradeAllowed,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="AccountProfileChanged")


@_attrs_define
class AccountProfileChanged:
    """`data` of an `account.profile_changed` message on the `events` channel: the terminal reads its account's slow facts
    (`AccountProfile`) every 60 seconds and sends this when any of them differs from what it last read, and when it has
    no earlier reading to compare with. Every fact is sent as it now stands; `changed` names the ones that moved. A fact
    the terminal could not read is left out. On the stream every value is text, as on every event.

        Attributes:
            schema_version (str): The payload's version; 1
            terminal_id (UUID):
            trade_allowed (AccountProfileChangedTradeAllowed): Whether the broker allows trading on the account
            expert_allowed (AccountProfileChangedExpertAllowed): Whether the broker allows expert advisors to trade on the
                account
            changed (str): A JSON array as text of the facts that moved since the last read: currency, leverage, company,
                account_type, margin_mode, trade_allowed, expert_allowed. All of them when there was no earlier reading
            observed_at (datetime.datetime): When the terminal read them, UTC
            currency (Union[Unset, str]): The account currency; absent when not read
            leverage (Union[Unset, str]): The account leverage, an integer as text (500 is 1:500); absent when not read
            company (Union[Unset, str]): The broker's company name as MT5 gives it; absent when not read
            account_type (Union[Unset, AccountProfileChangedAccountType]): Absent when not read
            margin_mode (Union[Unset, AccountProfileChangedMarginMode]): Absent when not read
    """

    schema_version: str
    terminal_id: UUID
    trade_allowed: AccountProfileChangedTradeAllowed
    expert_allowed: AccountProfileChangedExpertAllowed
    changed: str
    observed_at: datetime.datetime
    currency: Union[Unset, str] = UNSET
    leverage: Union[Unset, str] = UNSET
    company: Union[Unset, str] = UNSET
    account_type: Union[Unset, AccountProfileChangedAccountType] = UNSET
    margin_mode: Union[Unset, AccountProfileChangedMarginMode] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        schema_version = self.schema_version

        terminal_id = str(self.terminal_id)

        trade_allowed = self.trade_allowed.value

        expert_allowed = self.expert_allowed.value

        changed = self.changed

        observed_at = self.observed_at.isoformat()

        currency = self.currency

        leverage = self.leverage

        company = self.company

        account_type: Union[Unset, str] = UNSET
        if not isinstance(self.account_type, Unset):
            account_type = self.account_type.value

        margin_mode: Union[Unset, str] = UNSET
        if not isinstance(self.margin_mode, Unset):
            margin_mode = self.margin_mode.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "schema_version": schema_version,
                "terminal_id": terminal_id,
                "trade_allowed": trade_allowed,
                "expert_allowed": expert_allowed,
                "changed": changed,
                "observed_at": observed_at,
            }
        )
        if currency is not UNSET:
            field_dict["currency"] = currency
        if leverage is not UNSET:
            field_dict["leverage"] = leverage
        if company is not UNSET:
            field_dict["company"] = company
        if account_type is not UNSET:
            field_dict["account_type"] = account_type
        if margin_mode is not UNSET:
            field_dict["margin_mode"] = margin_mode

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        schema_version = d.pop("schema_version")

        terminal_id = UUID(d.pop("terminal_id"))

        trade_allowed = AccountProfileChangedTradeAllowed(d.pop("trade_allowed"))

        expert_allowed = AccountProfileChangedExpertAllowed(d.pop("expert_allowed"))

        changed = d.pop("changed")

        observed_at = isoparse(d.pop("observed_at"))

        currency = d.pop("currency", UNSET)

        leverage = d.pop("leverage", UNSET)

        company = d.pop("company", UNSET)

        _account_type = d.pop("account_type", UNSET)
        account_type: Union[Unset, AccountProfileChangedAccountType]
        if isinstance(_account_type, Unset):
            account_type = UNSET
        else:
            account_type = AccountProfileChangedAccountType(_account_type)

        _margin_mode = d.pop("margin_mode", UNSET)
        margin_mode: Union[Unset, AccountProfileChangedMarginMode]
        if isinstance(_margin_mode, Unset):
            margin_mode = UNSET
        else:
            margin_mode = AccountProfileChangedMarginMode(_margin_mode)

        account_profile_changed = cls(
            schema_version=schema_version,
            terminal_id=terminal_id,
            trade_allowed=trade_allowed,
            expert_allowed=expert_allowed,
            changed=changed,
            observed_at=observed_at,
            currency=currency,
            leverage=leverage,
            company=company,
            account_type=account_type,
            margin_mode=margin_mode,
        )

        account_profile_changed.additional_properties = d
        return account_profile_changed

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
