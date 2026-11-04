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
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="JournalLine")


@_attrs_define
class JournalLine:
    """
    Attributes:
        ts (datetime.datetime): UTC: the journal file's date and the line's time, converted from the cell's clock
        source (str): The journal's own source column as MetaTrader writes it, e.g. Network, Terminal, Trades
        message (str): The line as written, account numbers masked, file paths removed, at most 200 characters.
            MetaTrader's journal has no level column, so none is given
    """

    ts: datetime.datetime
    source: str
    message: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ts = self.ts.isoformat()

        source = self.source

        message = self.message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ts": ts,
                "source": source,
                "message": message,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ts = isoparse(d.pop("ts"))

        source = d.pop("source")

        message = d.pop("message")

        journal_line = cls(
            ts=ts,
            source=source,
            message=message,
        )

        journal_line.additional_properties = d
        return journal_line

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
