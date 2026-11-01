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

from ..models.candle_list_source import CandleListSource
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.candle import Candle


T = TypeVar("T", bound="CandleList")


@_attrs_define
class CandleList:
    """
    Attributes:
        items (list['Candle']): Oldest first by bar time; at most 1000 bars per call
        source (Union[Unset, CandleListSource]): Where the bars came from: the platform's store (no cell), one of your
            terminals, or closed bars from the store and the forming bar from a terminal
        complete_from (Union[None, Unset, datetime.datetime]): For an answer from the store: the oldest bar of the span
            the platform vouches holds every bar
        complete_to (Union[None, Unset, datetime.datetime]): For an answer from the store: the newest bar of that span.
            Holding bars up to it, you are missing none. Older than the last closed boundary while a gap is repaired, with
            Retry-After
    """

    items: list["Candle"]
    source: Union[Unset, CandleListSource] = UNSET
    complete_from: Union[None, Unset, datetime.datetime] = UNSET
    complete_to: Union[None, Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.candle import Candle

        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        source: Union[Unset, str] = UNSET
        if not isinstance(self.source, Unset):
            source = self.source.value

        complete_from: Union[None, Unset, str]
        if isinstance(self.complete_from, Unset):
            complete_from = UNSET
        elif isinstance(self.complete_from, datetime.datetime):
            complete_from = self.complete_from.isoformat()
        else:
            complete_from = self.complete_from

        complete_to: Union[None, Unset, str]
        if isinstance(self.complete_to, Unset):
            complete_to = UNSET
        elif isinstance(self.complete_to, datetime.datetime):
            complete_to = self.complete_to.isoformat()
        else:
            complete_to = self.complete_to

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "items": items,
            }
        )
        if source is not UNSET:
            field_dict["source"] = source
        if complete_from is not UNSET:
            field_dict["complete_from"] = complete_from
        if complete_to is not UNSET:
            field_dict["complete_to"] = complete_to

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.candle import Candle

        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = Candle.from_dict(items_item_data)

            items.append(items_item)

        _source = d.pop("source", UNSET)
        source: Union[Unset, CandleListSource]
        if isinstance(_source, Unset):
            source = UNSET
        else:
            source = CandleListSource(_source)

        def _parse_complete_from(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                complete_from_type_0 = isoparse(data)

                return complete_from_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        complete_from = _parse_complete_from(d.pop("complete_from", UNSET))

        def _parse_complete_to(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                complete_to_type_0 = isoparse(data)

                return complete_to_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        complete_to = _parse_complete_to(d.pop("complete_to", UNSET))

        candle_list = cls(
            items=items,
            source=source,
            complete_from=complete_from,
            complete_to=complete_to,
        )

        candle_list.additional_properties = d
        return candle_list

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
