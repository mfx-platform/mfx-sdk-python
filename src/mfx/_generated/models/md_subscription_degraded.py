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

from ..models.md_subscription_degraded_cause import MdSubscriptionDegradedCause
from ..models.md_subscription_degraded_reason import MdSubscriptionDegradedReason
from ..types import UNSET, Unset

T = TypeVar("T", bound="MdSubscriptionDegraded")


@_attrs_define
class MdSubscriptionDegraded:
    """`data` of an `md.subscription_degraded` message on the `events` channel: sent once when a subscription becomes
    degraded, whatever the cause. A reason or a cause that gives way to another while it stays degraded sends nothing;
    read the subscription for the reason and the cause that hold now.

        Attributes:
            schema_version (str):
            subscription_id (UUID):
            broker_id (UUID):
            server_id (UUID):
            symbol (str):
            reason (MdSubscriptionDegradedReason):
            cause (MdSubscriptionDegradedCause): Whose cause it is, as the subscription's `degraded_cause`; on a recovery,
                the cause it recovered from. Sent whatever the cause
            since (datetime.datetime):
            last_tick_at (Union[Unset, datetime.datetime]): The symbol's last tick; absent when it has not ticked
    """

    schema_version: str
    subscription_id: UUID
    broker_id: UUID
    server_id: UUID
    symbol: str
    reason: MdSubscriptionDegradedReason
    cause: MdSubscriptionDegradedCause
    since: datetime.datetime
    last_tick_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        schema_version = self.schema_version

        subscription_id = str(self.subscription_id)

        broker_id = str(self.broker_id)

        server_id = str(self.server_id)

        symbol = self.symbol

        reason = self.reason.value

        cause = self.cause.value

        since = self.since.isoformat()

        last_tick_at: Union[Unset, str] = UNSET
        if not isinstance(self.last_tick_at, Unset):
            last_tick_at = self.last_tick_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "schema_version": schema_version,
                "subscription_id": subscription_id,
                "broker_id": broker_id,
                "server_id": server_id,
                "symbol": symbol,
                "reason": reason,
                "cause": cause,
                "since": since,
            }
        )
        if last_tick_at is not UNSET:
            field_dict["last_tick_at"] = last_tick_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        schema_version = d.pop("schema_version")

        subscription_id = UUID(d.pop("subscription_id"))

        broker_id = UUID(d.pop("broker_id"))

        server_id = UUID(d.pop("server_id"))

        symbol = d.pop("symbol")

        reason = MdSubscriptionDegradedReason(d.pop("reason"))

        cause = MdSubscriptionDegradedCause(d.pop("cause"))

        since = isoparse(d.pop("since"))

        _last_tick_at = d.pop("last_tick_at", UNSET)
        last_tick_at: Union[Unset, datetime.datetime]
        if isinstance(_last_tick_at, Unset):
            last_tick_at = UNSET
        else:
            last_tick_at = isoparse(_last_tick_at)

        md_subscription_degraded = cls(
            schema_version=schema_version,
            subscription_id=subscription_id,
            broker_id=broker_id,
            server_id=server_id,
            symbol=symbol,
            reason=reason,
            cause=cause,
            since=since,
            last_tick_at=last_tick_at,
        )

        md_subscription_degraded.additional_properties = d
        return md_subscription_degraded

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
