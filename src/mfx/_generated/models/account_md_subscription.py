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

from ..models.account_md_subscription_state import AccountMdSubscriptionState
from ..types import UNSET, Unset

T = TypeVar("T", bound="AccountMdSubscription")


@_attrs_define
class AccountMdSubscription:
    """A cTrader account's market-data subscription

    Attributes:
        id (UUID): Stopped with DELETE /md/subscriptions/{id}
        account_id (UUID):
        symbol (str):
        state (AccountMdSubscriptionState): `pending` until the first spot after it; `streaming` once one has arrived
        created_at (datetime.datetime):
        first_tick_at (Union[None, Unset, datetime.datetime]):
    """

    id: UUID
    account_id: UUID
    symbol: str
    state: AccountMdSubscriptionState
    created_at: datetime.datetime
    first_tick_at: Union[None, Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        account_id = str(self.account_id)

        symbol = self.symbol

        state = self.state.value

        created_at = self.created_at.isoformat()

        first_tick_at: Union[None, Unset, str]
        if isinstance(self.first_tick_at, Unset):
            first_tick_at = UNSET
        elif isinstance(self.first_tick_at, datetime.datetime):
            first_tick_at = self.first_tick_at.isoformat()
        else:
            first_tick_at = self.first_tick_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "account_id": account_id,
                "symbol": symbol,
                "state": state,
                "created_at": created_at,
            }
        )
        if first_tick_at is not UNSET:
            field_dict["first_tick_at"] = first_tick_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        account_id = UUID(d.pop("account_id"))

        symbol = d.pop("symbol")

        state = AccountMdSubscriptionState(d.pop("state"))

        created_at = isoparse(d.pop("created_at"))

        def _parse_first_tick_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                first_tick_at_type_0 = isoparse(data)

                return first_tick_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        first_tick_at = _parse_first_tick_at(d.pop("first_tick_at", UNSET))

        account_md_subscription = cls(
            id=id,
            account_id=account_id,
            symbol=symbol,
            state=state,
            created_at=created_at,
            first_tick_at=first_tick_at,
        )

        account_md_subscription.additional_properties = d
        return account_md_subscription

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
