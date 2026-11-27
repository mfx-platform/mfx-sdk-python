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

from ..models.copy_close_entry_state import CopyCloseEntryState
from ..models.copy_close_entry_why_type_1 import CopyCloseEntryWhyType1
from ..models.copy_close_entry_why_type_2_type_1 import CopyCloseEntryWhyType2Type1
from ..models.copy_close_entry_why_type_3_type_1 import CopyCloseEntryWhyType3Type1
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.copy_close_attempt import CopyCloseAttempt


T = TypeVar("T", bound="CopyCloseEntry")


@_attrs_define
class CopyCloseEntry:
    """
    Attributes:
        position_id (Union[None, UUID]): The copied position on the ledger; null for a copy that filled after the close
            was asked and that the ledger had not recorded
        leader_position_ref (str):
        symbol (str): The follower's symbol
        volume (Union[None, str]): The copied volume asked to close, in the follower venue's unit
        state (CopyCloseEntryState):
        why (Union[CopyCloseEntryWhyType1, CopyCloseEntryWhyType2Type1, CopyCloseEntryWhyType3Type1, None]): Why it is
            not closed: a netting account its host cannot read, a position no copy of the follower opened, one opened after
            a group close's cutoff, or the close stopped at its give-up time
        cut (bool): The venue closed less than the copied volume: the account's own trading had already cut it
        closed_volume (str): The volume MFX Hub closed of it, every attempt together
        attempts (list['CopyCloseAttempt']):
    """

    position_id: Union[None, UUID]
    leader_position_ref: str
    symbol: str
    volume: Union[None, str]
    state: CopyCloseEntryState
    why: Union[
        CopyCloseEntryWhyType1, CopyCloseEntryWhyType2Type1, CopyCloseEntryWhyType3Type1, None
    ]
    cut: bool
    closed_volume: str
    attempts: list["CopyCloseAttempt"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.copy_close_attempt import CopyCloseAttempt

        position_id: Union[None, str]
        if isinstance(self.position_id, UUID):
            position_id = str(self.position_id)
        else:
            position_id = self.position_id

        leader_position_ref = self.leader_position_ref

        symbol = self.symbol

        volume: Union[None, str]
        volume = self.volume

        state = self.state.value

        why: Union[None, str]
        if isinstance(self.why, CopyCloseEntryWhyType1):
            why = self.why.value
        elif isinstance(self.why, CopyCloseEntryWhyType2Type1):
            why = self.why.value
        elif isinstance(self.why, CopyCloseEntryWhyType3Type1):
            why = self.why.value
        else:
            why = self.why

        cut = self.cut

        closed_volume = self.closed_volume

        attempts = []
        for attempts_item_data in self.attempts:
            attempts_item = attempts_item_data.to_dict()
            attempts.append(attempts_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "position_id": position_id,
                "leader_position_ref": leader_position_ref,
                "symbol": symbol,
                "volume": volume,
                "state": state,
                "why": why,
                "cut": cut,
                "closed_volume": closed_volume,
                "attempts": attempts,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.copy_close_attempt import CopyCloseAttempt

        d = dict(src_dict)

        def _parse_position_id(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                position_id_type_0 = UUID(data)

                return position_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        position_id = _parse_position_id(d.pop("position_id"))

        leader_position_ref = d.pop("leader_position_ref")

        symbol = d.pop("symbol")

        def _parse_volume(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        volume = _parse_volume(d.pop("volume"))

        state = CopyCloseEntryState._read(d.pop("state"))

        def _parse_why(
            data: object,
        ) -> Union[
            CopyCloseEntryWhyType1, CopyCloseEntryWhyType2Type1, CopyCloseEntryWhyType3Type1, None
        ]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                why_type_1 = CopyCloseEntryWhyType1._read(data)

                return why_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                why_type_2_type_1 = CopyCloseEntryWhyType2Type1._read(data)

                return why_type_2_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                why_type_3_type_1 = CopyCloseEntryWhyType3Type1._read(data)

                return why_type_3_type_1
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    CopyCloseEntryWhyType1,
                    CopyCloseEntryWhyType2Type1,
                    CopyCloseEntryWhyType3Type1,
                    None,
                ],
                data,
            )

        why = _parse_why(d.pop("why"))

        cut = d.pop("cut")

        closed_volume = d.pop("closed_volume")

        attempts = []
        _attempts = d.pop("attempts")
        for attempts_item_data in _attempts:
            attempts_item = CopyCloseAttempt.from_dict(attempts_item_data)

            attempts.append(attempts_item)

        copy_close_entry = cls(
            position_id=position_id,
            leader_position_ref=leader_position_ref,
            symbol=symbol,
            volume=volume,
            state=state,
            why=why,
            cut=cut,
            closed_volume=closed_volume,
            attempts=attempts,
        )

        copy_close_entry.additional_properties = d
        return copy_close_entry

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
