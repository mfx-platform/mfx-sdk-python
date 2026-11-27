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

from ..models.copy_signal_entry_action import CopySignalEntryAction
from ..models.copy_signal_entry_kind import CopySignalEntryKind
from ..models.copy_signal_entry_side import CopySignalEntrySide
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.copy_signal_entry_outcomes import CopySignalEntryOutcomes


T = TypeVar("T", bound="CopySignalEntry")


@_attrs_define
class CopySignalEntry:
    """One leader fill or external signal as MFX Hub recorded it, the console's own row, with what became of its copies;
    never its signature, its key id or the source's body

        Attributes:
            id (UUID):
            leader_id (UUID):
            kind (CopySignalEntryKind):
            action (CopySignalEntryAction):
            side (CopySignalEntrySide):
            volume_units (str): The leader's volume in base units, a decimal string
            price (Union[None, str]):
            sl (Union[None, str]):
            tp (Union[None, str]):
            instrument_key (Union[None, str]):
            leader_currency (Union[None, str]):
            source_id (Union[None, str]): The external source's own id, or the leader fill's id
            iat (datetime.datetime):
            exp (datetime.datetime):
            created_at (datetime.datetime):
            outcomes (CopySignalEntryOutcomes): How many of the signal's own copies, one a follower, were filled, refused
                and skipped; 0 where none. A stop-out's close names the signal it closes but is not its copy
    """

    id: UUID
    leader_id: UUID
    kind: CopySignalEntryKind
    action: CopySignalEntryAction
    side: CopySignalEntrySide
    volume_units: str
    price: Union[None, str]
    sl: Union[None, str]
    tp: Union[None, str]
    instrument_key: Union[None, str]
    leader_currency: Union[None, str]
    source_id: Union[None, str]
    iat: datetime.datetime
    exp: datetime.datetime
    created_at: datetime.datetime
    outcomes: "CopySignalEntryOutcomes"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.copy_signal_entry_outcomes import CopySignalEntryOutcomes

        id = str(self.id)

        leader_id = str(self.leader_id)

        kind = self.kind.value

        action = self.action.value

        side = self.side.value

        volume_units = self.volume_units

        price: Union[None, str]
        price = self.price

        sl: Union[None, str]
        sl = self.sl

        tp: Union[None, str]
        tp = self.tp

        instrument_key: Union[None, str]
        instrument_key = self.instrument_key

        leader_currency: Union[None, str]
        leader_currency = self.leader_currency

        source_id: Union[None, str]
        source_id = self.source_id

        iat = self.iat.isoformat()

        exp = self.exp.isoformat()

        created_at = self.created_at.isoformat()

        outcomes = self.outcomes.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "leader_id": leader_id,
                "kind": kind,
                "action": action,
                "side": side,
                "volume_units": volume_units,
                "price": price,
                "sl": sl,
                "tp": tp,
                "instrument_key": instrument_key,
                "leader_currency": leader_currency,
                "source_id": source_id,
                "iat": iat,
                "exp": exp,
                "created_at": created_at,
                "outcomes": outcomes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.copy_signal_entry_outcomes import CopySignalEntryOutcomes

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        leader_id = UUID(d.pop("leader_id"))

        kind = CopySignalEntryKind._read(d.pop("kind"))

        action = CopySignalEntryAction._read(d.pop("action"))

        side = CopySignalEntrySide._read(d.pop("side"))

        volume_units = d.pop("volume_units")

        def _parse_price(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        price = _parse_price(d.pop("price"))

        def _parse_sl(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        sl = _parse_sl(d.pop("sl"))

        def _parse_tp(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        tp = _parse_tp(d.pop("tp"))

        def _parse_instrument_key(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        instrument_key = _parse_instrument_key(d.pop("instrument_key"))

        def _parse_leader_currency(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        leader_currency = _parse_leader_currency(d.pop("leader_currency"))

        def _parse_source_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        source_id = _parse_source_id(d.pop("source_id"))

        iat = isoparse(d.pop("iat"))

        exp = isoparse(d.pop("exp"))

        created_at = isoparse(d.pop("created_at"))

        outcomes = CopySignalEntryOutcomes.from_dict(d.pop("outcomes"))

        copy_signal_entry = cls(
            id=id,
            leader_id=leader_id,
            kind=kind,
            action=action,
            side=side,
            volume_units=volume_units,
            price=price,
            sl=sl,
            tp=tp,
            instrument_key=instrument_key,
            leader_currency=leader_currency,
            source_id=source_id,
            iat=iat,
            exp=exp,
            created_at=created_at,
            outcomes=outcomes,
        )

        copy_signal_entry.additional_properties = d
        return copy_signal_entry

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
