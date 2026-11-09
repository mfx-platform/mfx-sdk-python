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

from ..models.copy_outcome import CopyOutcome
from ..models.copy_reason import CopyReason
from ..models.venue import Venue
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.copy_leader_deal import CopyLeaderDeal


T = TypeVar("T", bound="CopyRefused")


@_attrs_define
class CopyRefused:
    """`data` of `copy.refused`: one follower's copy did not fill (refused, skipped or a stop-out's close)

    Attributes:
        schema_version (str):
        signal_id (UUID):
        leader_id (UUID):
        follower_id (UUID):
        account_id (UUID):
        venue (Venue): The trading technology an account is on. A venue MFX Hub adds is a new value, so a client must
            read one it does not know
        deal (CopyLeaderDeal): The leader's deal a copy came from, in venue-neutral terms
        outcome (CopyOutcome): filled: the copy reached the venue and filled. refused: it was not sent, or the venue
            refused it; `reason` says why. skipped: the follower's own options left it out (skip_pending, close_only).
            stopout: a close made by a stop-out.
        reason (CopyReason): Why a copy did not fill. The list is closed: a new reason is a change to this contract.
            mapping: no follower symbol matched, or two did. min_volume: the scaled volume is under the follower's or the
            broker's minimum; it is never enlarged. no_stop: fixed_risk needs the leader's stop loss and there was none.
            risk_rule: a Risk Management rule on the follower account, or a leader or group limit, refused it. plan_limit: a
            Copy Trading limit of your plan. stopped_out: the follower is stopped out. signal_expired: the signal outlived
            its lifetime before it could be copied. skip_pending: the follower skips pending orders. close_only: the
            follower copies closes only. paused: the leader, the follower or its group is paused. account_not_connected: the
            follower account is not connected. market_closed: the symbol's market is closed. no_conversion: no current rate
            to convert the leader's figures into the follower account's currency. not_on_this_venue: the follower's venue
            cannot do what was asked. venue_unavailable: the venue did not answer. broker: the venue refused it; its own
            code is in `venue_code`.
        venue_code (Union[None, str]): The venue's own code beside broker
        why (Union[None, str]): The reason in words, for a person
        at (datetime.datetime):
    """

    schema_version: str
    signal_id: UUID
    leader_id: UUID
    follower_id: UUID
    account_id: UUID
    venue: Venue
    deal: "CopyLeaderDeal"
    outcome: CopyOutcome
    reason: CopyReason
    venue_code: Union[None, str]
    why: Union[None, str]
    at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.copy_leader_deal import CopyLeaderDeal

        schema_version = self.schema_version

        signal_id = str(self.signal_id)

        leader_id = str(self.leader_id)

        follower_id = str(self.follower_id)

        account_id = str(self.account_id)

        venue = self.venue.value

        deal = self.deal.to_dict()

        outcome = self.outcome.value

        reason = self.reason.value

        venue_code: Union[None, str]
        venue_code = self.venue_code

        why: Union[None, str]
        why = self.why

        at = self.at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "schema_version": schema_version,
                "signal_id": signal_id,
                "leader_id": leader_id,
                "follower_id": follower_id,
                "account_id": account_id,
                "venue": venue,
                "deal": deal,
                "outcome": outcome,
                "reason": reason,
                "venue_code": venue_code,
                "why": why,
                "at": at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.copy_leader_deal import CopyLeaderDeal

        d = dict(src_dict)
        schema_version = d.pop("schema_version")

        signal_id = UUID(d.pop("signal_id"))

        leader_id = UUID(d.pop("leader_id"))

        follower_id = UUID(d.pop("follower_id"))

        account_id = UUID(d.pop("account_id"))

        venue = Venue(d.pop("venue"))

        deal = CopyLeaderDeal.from_dict(d.pop("deal"))

        outcome = CopyOutcome(d.pop("outcome"))

        reason = CopyReason(d.pop("reason"))

        def _parse_venue_code(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        venue_code = _parse_venue_code(d.pop("venue_code"))

        def _parse_why(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        why = _parse_why(d.pop("why"))

        at = isoparse(d.pop("at"))

        copy_refused = cls(
            schema_version=schema_version,
            signal_id=signal_id,
            leader_id=leader_id,
            follower_id=follower_id,
            account_id=account_id,
            venue=venue,
            deal=deal,
            outcome=outcome,
            reason=reason,
            venue_code=venue_code,
            why=why,
            at=at,
        )

        copy_refused.additional_properties = d
        return copy_refused

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
