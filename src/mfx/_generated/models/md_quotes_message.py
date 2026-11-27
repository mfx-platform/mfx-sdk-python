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

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.md_server_quote import MdServerQuote


T = TypeVar("T", bound="MdQuotesMessage")


@_attrs_define
class MdQuotesMessage:
    """`data` of an `md.quotes` message on `md:{server_id}`: the quotes of the server's symbols that changed since the last
    message, each symbol at most once, with its newest quote. A symbol that did not tick is not in it, and the ticks
    between two messages are not sent on this channel: a tenant that needs every tick subscribes to the symbol's own
    channel. When more than 500 symbols changed, several messages follow one another, each complete in itself. A message
    with `snapshot` true answers `subscribe` or `resume`: it carries the newest quote the platform received for each
    symbol in the last 24 hours, which may be old (read its `broker_ts`), and has no `seq`. A client keeps, for each
    symbol, the quote with the newer `broker_ts`. Nothing is sent while nothing changes. `seq` increases from one
    message to the next and is not consecutive, so it does not show a lost message; a symbol is current again at its
    next tick, or at once by subscribing again. A client that reads slowly is not sent a backlog: the quotes waiting for
    it are kept one a symbol, the newest, and sent when it reads. When more than 500 of them wait they are sent as
    several messages, and only the last of those carries `seq`. `md_msgs_per_s` counts the channel's entries, each of up
    to 500 quotes, not its quotes.

        Attributes:
            schema_version (str): The payload's version; 1
            interval_ms (int): The interval this message was built to: the subscription's `interval_ms` when it was sent
            snapshot (bool): True on the messages that answer `subscribe` or `resume`; false on a change
            quotes (list['MdServerQuote']):
            fanned_at (str): When the platform wrote this message to the tenant's stream, or read the snapshot: seconds
                since 1970 UTC with milliseconds, as text. A message that gathers several waiting flushes for a slow reader says
                the newest of them here, as it does in `interval_ms` and `seq`; each quote's own age is in its `source_sent_at`
                and `broker_ts`
            sent_at (Union[Unset, str]): When the gateway put the message on this connection, in the form of `fanned_at`
    """

    schema_version: str
    interval_ms: int
    snapshot: bool
    quotes: list["MdServerQuote"]
    fanned_at: str
    sent_at: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.md_server_quote import MdServerQuote

        schema_version = self.schema_version

        interval_ms = self.interval_ms

        snapshot = self.snapshot

        quotes = []
        for quotes_item_data in self.quotes:
            quotes_item = quotes_item_data.to_dict()
            quotes.append(quotes_item)

        fanned_at = self.fanned_at

        sent_at = self.sent_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "schema_version": schema_version,
                "interval_ms": interval_ms,
                "snapshot": snapshot,
                "quotes": quotes,
                "fanned_at": fanned_at,
            }
        )
        if sent_at is not UNSET:
            field_dict["sent_at"] = sent_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.md_server_quote import MdServerQuote

        d = dict(src_dict)
        schema_version = d.pop("schema_version")

        interval_ms = d.pop("interval_ms")

        snapshot = d.pop("snapshot")

        quotes = []
        _quotes = d.pop("quotes")
        for quotes_item_data in _quotes:
            quotes_item = MdServerQuote.from_dict(quotes_item_data)

            quotes.append(quotes_item)

        fanned_at = d.pop("fanned_at")

        sent_at = d.pop("sent_at", UNSET)

        md_quotes_message = cls(
            schema_version=schema_version,
            interval_ms=interval_ms,
            snapshot=snapshot,
            quotes=quotes,
            fanned_at=fanned_at,
            sent_at=sent_at,
        )

        md_quotes_message.additional_properties = d
        return md_quotes_message

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
