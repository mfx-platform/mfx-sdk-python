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

from ..models.webhook_endpoint_update_status import WebhookEndpointUpdateStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="WebhookEndpointUpdate")


@_attrs_define
class WebhookEndpointUpdate:
    """Fields left out keep their value. `status: active` resumes an endpoint paused by the tenant, an operator or the
    platform; `paused` pauses it

        Attributes:
            url (Union[Unset, str]):
            event_types (Union[Unset, list[str]]):
            description (Union[None, Unset, str]):
            status (Union[Unset, WebhookEndpointUpdateStatus]):
    """

    url: Union[Unset, str] = UNSET
    event_types: Union[Unset, list[str]] = UNSET
    description: Union[None, Unset, str] = UNSET
    status: Union[Unset, WebhookEndpointUpdateStatus] = UNSET

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        event_types: Union[Unset, list[str]] = UNSET
        if not isinstance(self.event_types, Unset):
            event_types = self.event_types

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if url is not UNSET:
            field_dict["url"] = url
        if event_types is not UNSET:
            field_dict["event_types"] = event_types
        if description is not UNSET:
            field_dict["description"] = description
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url", UNSET)

        event_types = cast(list[str], d.pop("event_types", UNSET))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        _status = d.pop("status", UNSET)
        status: Union[Unset, WebhookEndpointUpdateStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = WebhookEndpointUpdateStatus(_status)

        webhook_endpoint_update = cls(
            url=url,
            event_types=event_types,
            description=description,
            status=status,
        )

        return webhook_endpoint_update
