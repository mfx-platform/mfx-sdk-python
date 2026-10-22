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

T = TypeVar("T", bound="WebhookEndpointCreate")


@_attrs_define
class WebhookEndpointCreate:
    """An address MFX Hub calls for the tenant's events. `https` only, port 443 or 8443, a host name and not an address, no
    credentials in the URL; a name that resolves to a private, loopback, link-local, metadata or MFX Hub address is
    refused with 422. The number of endpoints a tenant may have is limited (409 `quota_exceeded`). Each delivery's body
    is the event as the `events` channel carries its `data`: `type`, the fields of the schema `x-event-payloads` on
    `/stream` names for that type, and `id`, the event's cursor (`MFX-Event-Id`).

        Attributes:
            url (str):
            event_types (list[str]): Event types as the events channel names them (`position.closed`), a family
                (`terminal.*`), or `*` for all. Ticks and candles are not events and are never sent this way
            description (Union[None, Unset, str]):
    """

    url: str
    event_types: list[str]
    description: Union[None, Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        event_types = self.event_types

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "url": url,
                "event_types": event_types,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        event_types = cast(list[str], d.pop("event_types"))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        webhook_endpoint_create = cls(
            url=url,
            event_types=event_types,
            description=description,
        )

        return webhook_endpoint_create
