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

from ..models.copy_log_entry_action import CopyLogEntryAction
from ..models.copy_log_entry_side import CopyLogEntrySide
from ..models.copy_outcome import CopyOutcome
from ..models.copy_reason import CopyReason
from ..models.venue import Venue
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.copy_stages import CopyStages


T = TypeVar("T", bound="CopyLogEntry")


@_attrs_define
class CopyLogEntry:
    """
    Attributes:
        id (UUID):
        created_at (datetime.datetime): The signal's time; every row of one signal carries it
        signal_id (UUID):
        leader_id (UUID):
        follower_id (UUID):
        account_id (UUID): The follower account
        venue (Venue): The trading technology an account is on. A venue MFX Hub adds is a new value, so a client must
            read one it does not know
        action (CopyLogEntryAction): What the leader did
        side (CopyLogEntrySide):
        instrument_key (Union[None, str]):
        outcome (CopyOutcome): filled: the copy reached the venue and filled. refused: it was not sent, or the venue
            refused it; `reason` says why. skipped: the follower's own options left it out (skip_pending, close_only).
            stopout: a close made by a stop-out.
        reason (Union[CopyReason, None]): Null exactly when filled
        venue_code (Union[None, str]): The venue's own code beside broker, as the venue gave it
        command_id (Union[None, UUID]): The command the copy became; GET /commands/{id} has it
        copied_volume (Union[None, str]): In the follower venue's unit
        price (Union[None, str]):
        slippage (Union[None, str]): The follower's fill price less the leader's, as a price distance; positive is worse
            for the follower
        stages (CopyStages): Milliseconds each stage took, each measured on its own machine. A stage that did not happen
            for this copy is absent. broker_ms is the venue's time and is not MFX Hub's.
        mfx_ms (Union[None, float]): MFX Hub's part: every stage but broker_ms, added up
        signal_to_order_ms (Union[None, float]): deliver_ms + expand_ms + queue_ms + hand_ms: from a held signal to the
            order call
    """

    id: UUID
    created_at: datetime.datetime
    signal_id: UUID
    leader_id: UUID
    follower_id: UUID
    account_id: UUID
    venue: Venue
    action: CopyLogEntryAction
    side: CopyLogEntrySide
    instrument_key: Union[None, str]
    outcome: CopyOutcome
    reason: Union[CopyReason, None]
    venue_code: Union[None, str]
    command_id: Union[None, UUID]
    copied_volume: Union[None, str]
    price: Union[None, str]
    slippage: Union[None, str]
    stages: "CopyStages"
    mfx_ms: Union[None, float]
    signal_to_order_ms: Union[None, float]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.copy_stages import CopyStages

        id = str(self.id)

        created_at = self.created_at.isoformat()

        signal_id = str(self.signal_id)

        leader_id = str(self.leader_id)

        follower_id = str(self.follower_id)

        account_id = str(self.account_id)

        venue = self.venue.value

        action = self.action.value

        side = self.side.value

        instrument_key: Union[None, str]
        instrument_key = self.instrument_key

        outcome = self.outcome.value

        reason: Union[None, str]
        if isinstance(self.reason, CopyReason):
            reason = self.reason.value
        else:
            reason = self.reason

        venue_code: Union[None, str]
        venue_code = self.venue_code

        command_id: Union[None, str]
        if isinstance(self.command_id, UUID):
            command_id = str(self.command_id)
        else:
            command_id = self.command_id

        copied_volume: Union[None, str]
        copied_volume = self.copied_volume

        price: Union[None, str]
        price = self.price

        slippage: Union[None, str]
        slippage = self.slippage

        stages = self.stages.to_dict()

        mfx_ms: Union[None, float]
        mfx_ms = self.mfx_ms

        signal_to_order_ms: Union[None, float]
        signal_to_order_ms = self.signal_to_order_ms

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "created_at": created_at,
                "signal_id": signal_id,
                "leader_id": leader_id,
                "follower_id": follower_id,
                "account_id": account_id,
                "venue": venue,
                "action": action,
                "side": side,
                "instrument_key": instrument_key,
                "outcome": outcome,
                "reason": reason,
                "venue_code": venue_code,
                "command_id": command_id,
                "copied_volume": copied_volume,
                "price": price,
                "slippage": slippage,
                "stages": stages,
                "mfx_ms": mfx_ms,
                "signal_to_order_ms": signal_to_order_ms,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.copy_stages import CopyStages

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        created_at = isoparse(d.pop("created_at"))

        signal_id = UUID(d.pop("signal_id"))

        leader_id = UUID(d.pop("leader_id"))

        follower_id = UUID(d.pop("follower_id"))

        account_id = UUID(d.pop("account_id"))

        venue = Venue(d.pop("venue"))

        action = CopyLogEntryAction(d.pop("action"))

        side = CopyLogEntrySide(d.pop("side"))

        def _parse_instrument_key(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        instrument_key = _parse_instrument_key(d.pop("instrument_key"))

        outcome = CopyOutcome(d.pop("outcome"))

        def _parse_reason(data: object) -> Union[CopyReason, None]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                reason_type_0 = CopyReason(data)

                return reason_type_0
            except:  # noqa: E722
                pass
            return cast(Union[CopyReason, None], data)

        reason = _parse_reason(d.pop("reason"))

        def _parse_venue_code(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        venue_code = _parse_venue_code(d.pop("venue_code"))

        def _parse_command_id(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                command_id_type_0 = UUID(data)

                return command_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        command_id = _parse_command_id(d.pop("command_id"))

        def _parse_copied_volume(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        copied_volume = _parse_copied_volume(d.pop("copied_volume"))

        def _parse_price(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        price = _parse_price(d.pop("price"))

        def _parse_slippage(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        slippage = _parse_slippage(d.pop("slippage"))

        stages = CopyStages.from_dict(d.pop("stages"))

        def _parse_mfx_ms(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        mfx_ms = _parse_mfx_ms(d.pop("mfx_ms"))

        def _parse_signal_to_order_ms(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        signal_to_order_ms = _parse_signal_to_order_ms(d.pop("signal_to_order_ms"))

        copy_log_entry = cls(
            id=id,
            created_at=created_at,
            signal_id=signal_id,
            leader_id=leader_id,
            follower_id=follower_id,
            account_id=account_id,
            venue=venue,
            action=action,
            side=side,
            instrument_key=instrument_key,
            outcome=outcome,
            reason=reason,
            venue_code=venue_code,
            command_id=command_id,
            copied_volume=copied_volume,
            price=price,
            slippage=slippage,
            stages=stages,
            mfx_ms=mfx_ms,
            signal_to_order_ms=signal_to_order_ms,
        )

        copy_log_entry.additional_properties = d
        return copy_log_entry

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
