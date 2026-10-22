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
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.webhook_endpoint_paused_by import WebhookEndpointPausedBy
from ..types import UNSET, Unset

T = TypeVar("T", bound="WebhookEndpointPaused")


@_attrs_define
class WebhookEndpointPaused:
    """`data` of a `webhook.endpoint_paused` message on the `events` channel

    Attributes:
        schema_version (str):
        endpoint_id (UUID):
        by (WebhookEndpointPausedBy):
        reason (str):
        at (datetime.datetime):
    """

    schema_version: str
    endpoint_id: UUID
    by: WebhookEndpointPausedBy
    reason: str
    at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        schema_version = self.schema_version

        endpoint_id = str(self.endpoint_id)

        by = self.by.value

        reason = self.reason

        at = self.at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "schema_version": schema_version,
                "endpoint_id": endpoint_id,
                "by": by,
                "reason": reason,
                "at": at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        schema_version = d.pop("schema_version")

        endpoint_id = UUID(d.pop("endpoint_id"))

        by = WebhookEndpointPausedBy(d.pop("by"))

        reason = d.pop("reason")

        at = isoparse(d.pop("at"))

        webhook_endpoint_paused = cls(
            schema_version=schema_version,
            endpoint_id=endpoint_id,
            by=by,
            reason=reason,
            at=at,
        )

        webhook_endpoint_paused.additional_properties = d
        return webhook_endpoint_paused

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
