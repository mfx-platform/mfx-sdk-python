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

from ..models.copy_close_attempt_outcome import CopyCloseAttemptOutcome
from ..types import UNSET, Unset

T = TypeVar("T", bound="CopyCloseAttempt")


@_attrs_define
class CopyCloseAttempt:
    """
    Attributes:
        close_id (UUID): The close whose order it was: a position carried over from a superseded close keeps that
            close's attempts
        attempt (int):
        command_id (Union[None, UUID]): The close order's command; null where the account's positions settled an attempt
            that had no answer
        outcome (CopyCloseAttemptOutcome):
        reason (Union[None, str]): On a refusal: signal_expired, expired, account_not_connected, not_current,
            margin_mode_unknown, market_closed, broker, already_closed, position_not_open (the venue says the position is
            not open), netting, not_copied or copy_mismatch (opened after a group close's cutoff)
        venue_code (Union[None, str]): The venue's own code beside broker
        volume_closed (Union[None, str]): On a fill, the volume the venue closed, in the follower venue's unit
        volume_after (Union[None, str]): The venue's volume of the position after the close; null when it is gone or was
            not read
        at (datetime.datetime):
    """

    close_id: UUID
    attempt: int
    command_id: Union[None, UUID]
    outcome: CopyCloseAttemptOutcome
    reason: Union[None, str]
    venue_code: Union[None, str]
    volume_closed: Union[None, str]
    volume_after: Union[None, str]
    at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        close_id = str(self.close_id)

        attempt = self.attempt

        command_id: Union[None, str]
        if isinstance(self.command_id, UUID):
            command_id = str(self.command_id)
        else:
            command_id = self.command_id

        outcome = self.outcome.value

        reason: Union[None, str]
        reason = self.reason

        venue_code: Union[None, str]
        venue_code = self.venue_code

        volume_closed: Union[None, str]
        volume_closed = self.volume_closed

        volume_after: Union[None, str]
        volume_after = self.volume_after

        at = self.at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "close_id": close_id,
                "attempt": attempt,
                "command_id": command_id,
                "outcome": outcome,
                "reason": reason,
                "venue_code": venue_code,
                "volume_closed": volume_closed,
                "volume_after": volume_after,
                "at": at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        close_id = UUID(d.pop("close_id"))

        attempt = d.pop("attempt")

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

        outcome = CopyCloseAttemptOutcome._read(d.pop("outcome"))

        def _parse_reason(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        reason = _parse_reason(d.pop("reason"))

        def _parse_venue_code(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        venue_code = _parse_venue_code(d.pop("venue_code"))

        def _parse_volume_closed(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        volume_closed = _parse_volume_closed(d.pop("volume_closed"))

        def _parse_volume_after(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        volume_after = _parse_volume_after(d.pop("volume_after"))

        at = isoparse(d.pop("at"))

        copy_close_attempt = cls(
            close_id=close_id,
            attempt=attempt,
            command_id=command_id,
            outcome=outcome,
            reason=reason,
            venue_code=venue_code,
            volume_closed=volume_closed,
            volume_after=volume_after,
            at=at,
        )

        copy_close_attempt.additional_properties = d
        return copy_close_attempt

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
