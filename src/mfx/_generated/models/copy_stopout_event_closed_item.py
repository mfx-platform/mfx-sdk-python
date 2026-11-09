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

from ..types import UNSET, Unset

T = TypeVar("T", bound="CopyStopoutEventClosedItem")


@_attrs_define
class CopyStopoutEventClosedItem:
    """
    Attributes:
        symbol (str):
        volume (str):
        command_id (Union[None, UUID]):
    """

    symbol: str
    volume: str
    command_id: Union[None, UUID]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        symbol = self.symbol

        volume = self.volume

        command_id: Union[None, str]
        if isinstance(self.command_id, UUID):
            command_id = str(self.command_id)
        else:
            command_id = self.command_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "symbol": symbol,
                "volume": volume,
                "command_id": command_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        symbol = d.pop("symbol")

        volume = d.pop("volume")

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

        copy_stopout_event_closed_item = cls(
            symbol=symbol,
            volume=volume,
            command_id=command_id,
        )

        copy_stopout_event_closed_item.additional_properties = d
        return copy_stopout_event_closed_item

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
