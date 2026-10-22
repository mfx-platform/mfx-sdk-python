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

from ..models.md_status_message_status import MdStatusMessageStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="MdStatusMessage")


@_attrs_define
class MdStatusMessage:
    """`data` of an `md.status` message on an `md:`, `candles:` or `book:` channel: whether the tenant's market data is
    held by a planned maintenance window. A window in progress that suspends `market_data` for the tenant sends
    `maintenance` on each of its open market data channels, and on each one subscribed or resumed while it holds (after
    the `ack`); no tick, candle or book is sent on them until it ends, and none of what arrived meanwhile is replayed.
    When the window ends, or the platform can no longer tell that it holds (maintenance fails open), `live` is sent and
    data flows again; a `book:` channel then sends the newest book first. A change of the window's end while it holds
    sends `maintenance` again with the new `ends_at`. The channel stays subscribed throughout; nothing is sent while the
    data is not held, so a channel that never sees one is live. `events`, `results:`, `account:` and `ea:` are not held
    by `market_data`.

        Attributes:
            schema_version (str): The payload's version; 1
            status (MdStatusMessageStatus): `maintenance` while a window holds the channel's data; `live` once it no longer
                does
            window_id (Union[None, UUID]): The window that holds it (where two do, the one ending last); null when `live`
            window (Union[None, str]): Its label, as the maintenance reads name it (`MW-0031`); null when `live`
            ends_at (Union[None, datetime.datetime]): The window's current end: its ETA while it runs, else its announced
                end; null when `live`
    """

    schema_version: str
    status: MdStatusMessageStatus
    window_id: Union[None, UUID]
    window: Union[None, str]
    ends_at: Union[None, datetime.datetime]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        schema_version = self.schema_version

        status = self.status.value

        window_id: Union[None, str]
        if isinstance(self.window_id, UUID):
            window_id = str(self.window_id)
        else:
            window_id = self.window_id

        window: Union[None, str]
        window = self.window

        ends_at: Union[None, str]
        if isinstance(self.ends_at, datetime.datetime):
            ends_at = self.ends_at.isoformat()
        else:
            ends_at = self.ends_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "schema_version": schema_version,
                "status": status,
                "window_id": window_id,
                "window": window,
                "ends_at": ends_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        schema_version = d.pop("schema_version")

        status = MdStatusMessageStatus(d.pop("status"))

        def _parse_window_id(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                window_id_type_0 = UUID(data)

                return window_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        window_id = _parse_window_id(d.pop("window_id"))

        def _parse_window(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        window = _parse_window(d.pop("window"))

        def _parse_ends_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                ends_at_type_0 = isoparse(data)

                return ends_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        ends_at = _parse_ends_at(d.pop("ends_at"))

        md_status_message = cls(
            schema_version=schema_version,
            status=status,
            window_id=window_id,
            window=window,
            ends_at=ends_at,
        )

        md_status_message.additional_properties = d
        return md_status_message

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
