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

from ..types import UNSET, Unset

T = TypeVar("T", bound="BookMessage")


@_attrs_define
class BookMessage:
    """`data` of an `md.book` message on `book:{server_id}:{symbol}`: the symbol's whole order book as one of the tenant's
    terminals read it, best price first on each side. Replace your book with every message. The terminal reads at its
    refresh rate and sends a book only when it differs from the last it sent, so two changes inside one read are one
    book. `seq` increases as on `md:`; a gap is a book that was superseded before it reached you. Not a reconstruction:
    MFX Hub builds no book from ticks or from several terminals.

        Attributes:
            schema_version (str): The payload's version; 1
            bids (list[list[str]]): Buy orders, highest price first, at most `levels`: `[price, volume]`, decimals as
                strings
            asks (list[list[str]]): Sell orders, lowest price first, at most `levels`: `[price, volume]`, decimals as
                strings
            broker_ts (str): When the terminal read the book, on the broker's clock, to the millisecond (as a tick's
                `broker_ts`)
            levels (int): The most levels a side the platform reads: a side shorter than this is the whole of that side of
                the broker's book
    """

    schema_version: str
    bids: list[list[str]]
    asks: list[list[str]]
    broker_ts: str
    levels: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        schema_version = self.schema_version

        bids = []
        for bids_item_data in self.bids:
            bids_item = bids_item_data

            bids.append(bids_item)

        asks = []
        for asks_item_data in self.asks:
            asks_item = asks_item_data

            asks.append(asks_item)

        broker_ts = self.broker_ts

        levels = self.levels

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "schema_version": schema_version,
                "bids": bids,
                "asks": asks,
                "broker_ts": broker_ts,
                "levels": levels,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        schema_version = d.pop("schema_version")

        bids = []
        _bids = d.pop("bids")
        for bids_item_data in _bids:
            bids_item = cast(list[str], bids_item_data)

            bids.append(bids_item)

        asks = []
        _asks = d.pop("asks")
        for asks_item_data in _asks:
            asks_item = cast(list[str], asks_item_data)

            asks.append(asks_item)

        broker_ts = d.pop("broker_ts")

        levels = d.pop("levels")

        book_message = cls(
            schema_version=schema_version,
            bids=bids,
            asks=asks,
            broker_ts=broker_ts,
            levels=levels,
        )

        book_message.additional_properties = d
        return book_message

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
