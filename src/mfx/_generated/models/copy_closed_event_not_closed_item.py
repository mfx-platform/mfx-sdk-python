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

from ..models.copy_closed_event_not_closed_item_why_type_1 import (
    CopyClosedEventNotClosedItemWhyType1,
)
from ..models.copy_closed_event_not_closed_item_why_type_2_type_1 import (
    CopyClosedEventNotClosedItemWhyType2Type1,
)
from ..models.copy_closed_event_not_closed_item_why_type_3_type_1 import (
    CopyClosedEventNotClosedItemWhyType3Type1,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="CopyClosedEventNotClosedItem")


@_attrs_define
class CopyClosedEventNotClosedItem:
    """
    Attributes:
        symbol (str):
        volume (Union[None, str]):
        why (Union[CopyClosedEventNotClosedItemWhyType1, CopyClosedEventNotClosedItemWhyType2Type1,
            CopyClosedEventNotClosedItemWhyType3Type1, None]):
    """

    symbol: str
    volume: Union[None, str]
    why: Union[
        CopyClosedEventNotClosedItemWhyType1,
        CopyClosedEventNotClosedItemWhyType2Type1,
        CopyClosedEventNotClosedItemWhyType3Type1,
        None,
    ]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        symbol = self.symbol

        volume: Union[None, str]
        volume = self.volume

        why: Union[None, str]
        if isinstance(self.why, CopyClosedEventNotClosedItemWhyType1):
            why = self.why.value
        elif isinstance(self.why, CopyClosedEventNotClosedItemWhyType2Type1):
            why = self.why.value
        elif isinstance(self.why, CopyClosedEventNotClosedItemWhyType3Type1):
            why = self.why.value
        else:
            why = self.why

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "symbol": symbol,
                "volume": volume,
                "why": why,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        symbol = d.pop("symbol")

        def _parse_volume(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        volume = _parse_volume(d.pop("volume"))

        def _parse_why(
            data: object,
        ) -> Union[
            CopyClosedEventNotClosedItemWhyType1,
            CopyClosedEventNotClosedItemWhyType2Type1,
            CopyClosedEventNotClosedItemWhyType3Type1,
            None,
        ]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                why_type_1 = CopyClosedEventNotClosedItemWhyType1._read(data)

                return why_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                why_type_2_type_1 = CopyClosedEventNotClosedItemWhyType2Type1._read(data)

                return why_type_2_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                why_type_3_type_1 = CopyClosedEventNotClosedItemWhyType3Type1._read(data)

                return why_type_3_type_1
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    CopyClosedEventNotClosedItemWhyType1,
                    CopyClosedEventNotClosedItemWhyType2Type1,
                    CopyClosedEventNotClosedItemWhyType3Type1,
                    None,
                ],
                data,
            )

        why = _parse_why(d.pop("why"))

        copy_closed_event_not_closed_item = cls(
            symbol=symbol,
            volume=volume,
            why=why,
        )

        copy_closed_event_not_closed_item.additional_properties = d
        return copy_closed_event_not_closed_item

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
