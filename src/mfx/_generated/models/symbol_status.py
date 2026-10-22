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

from ..models.symbol_state import SymbolState
from ..models.symbol_status_reason_type_1 import SymbolStatusReasonType1
from ..models.symbol_status_reason_type_2_type_1 import SymbolStatusReasonType2Type1
from ..models.symbol_status_reason_type_3_type_1 import SymbolStatusReasonType3Type1
from ..types import UNSET, Unset

T = TypeVar("T", bound="SymbolStatus")


@_attrs_define
class SymbolStatus:
    """
    Attributes:
        state (SymbolState): Checked in this order, first match wins: unknown (no terminal of the tenant on this server
            is connected, or the newest symbol report from one is older than 180 s by default — could-not-read is never
            reported as closed) → trade_disabled → closed_session (broker time outside this weekday's trade sessions) →
            paused (inside trade sessions, a watched symbol with no tick for 300 s by default) → close_only → long_only /
            short_only → open.
        reason (Union[None, SymbolStatusReasonType1, SymbolStatusReasonType2Type1, SymbolStatusReasonType3Type1]): null
            when open.
        since (Union[None, datetime.datetime]): when the current state began, where known
        next_open (Union[None, datetime.datetime]): closed_session only — the next trade-session start, UTC
        last_tick_age_s (Union[None, float]): null when the symbol is not watched
        quote_watched (bool): True when a terminal of the tenant has this symbol in its instruments, so tick age is
            known and `paused` can be detected. An unwatched symbol is never reported paused.
        as_of (datetime.datetime): when this status was worked out
    """

    state: SymbolState
    reason: Union[
        None, SymbolStatusReasonType1, SymbolStatusReasonType2Type1, SymbolStatusReasonType3Type1
    ]
    since: Union[None, datetime.datetime]
    next_open: Union[None, datetime.datetime]
    last_tick_age_s: Union[None, float]
    quote_watched: bool
    as_of: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        state = self.state.value

        reason: Union[None, str]
        if isinstance(self.reason, SymbolStatusReasonType1):
            reason = self.reason.value
        elif isinstance(self.reason, SymbolStatusReasonType2Type1):
            reason = self.reason.value
        elif isinstance(self.reason, SymbolStatusReasonType3Type1):
            reason = self.reason.value
        else:
            reason = self.reason

        since: Union[None, str]
        if isinstance(self.since, datetime.datetime):
            since = self.since.isoformat()
        else:
            since = self.since

        next_open: Union[None, str]
        if isinstance(self.next_open, datetime.datetime):
            next_open = self.next_open.isoformat()
        else:
            next_open = self.next_open

        last_tick_age_s: Union[None, float]
        last_tick_age_s = self.last_tick_age_s

        quote_watched = self.quote_watched

        as_of = self.as_of.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "state": state,
                "reason": reason,
                "since": since,
                "next_open": next_open,
                "last_tick_age_s": last_tick_age_s,
                "quote_watched": quote_watched,
                "as_of": as_of,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        state = SymbolState(d.pop("state"))

        def _parse_reason(
            data: object,
        ) -> Union[
            None,
            SymbolStatusReasonType1,
            SymbolStatusReasonType2Type1,
            SymbolStatusReasonType3Type1,
        ]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                reason_type_1 = SymbolStatusReasonType1(data)

                return reason_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                reason_type_2_type_1 = SymbolStatusReasonType2Type1(data)

                return reason_type_2_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                reason_type_3_type_1 = SymbolStatusReasonType3Type1(data)

                return reason_type_3_type_1
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    None,
                    SymbolStatusReasonType1,
                    SymbolStatusReasonType2Type1,
                    SymbolStatusReasonType3Type1,
                ],
                data,
            )

        reason = _parse_reason(d.pop("reason"))

        def _parse_since(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                since_type_0 = isoparse(data)

                return since_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        since = _parse_since(d.pop("since"))

        def _parse_next_open(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                next_open_type_0 = isoparse(data)

                return next_open_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        next_open = _parse_next_open(d.pop("next_open"))

        def _parse_last_tick_age_s(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        last_tick_age_s = _parse_last_tick_age_s(d.pop("last_tick_age_s"))

        quote_watched = d.pop("quote_watched")

        as_of = isoparse(d.pop("as_of"))

        symbol_status = cls(
            state=state,
            reason=reason,
            since=since,
            next_open=next_open,
            last_tick_age_s=last_tick_age_s,
            quote_watched=quote_watched,
            as_of=as_of,
        )

        symbol_status.additional_properties = d
        return symbol_status

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
