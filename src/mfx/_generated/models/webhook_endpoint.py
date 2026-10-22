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

from ..models.webhook_endpoint_paused_by_type_1 import WebhookEndpointPausedByType1
from ..models.webhook_endpoint_paused_by_type_2_type_1 import (
    WebhookEndpointPausedByType2Type1,
)
from ..models.webhook_endpoint_paused_by_type_3_type_1 import (
    WebhookEndpointPausedByType3Type1,
)
from ..models.webhook_endpoint_status import WebhookEndpointStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="WebhookEndpoint")


@_attrs_define
class WebhookEndpoint:
    """One endpoint and how it is doing. A delivery that worked is a count and a time, never a record; what did not arrive
    is read from its failures. Never the secret.

        Attributes:
            id (UUID):
            url (str):
            event_types (list[str]):
            description (Union[None, str]):
            status (WebhookEndpointStatus):
            paused_reason (Union[None, str]): Why it is paused, in words; null while active
            paused_by (Union[None, WebhookEndpointPausedByType1, WebhookEndpointPausedByType2Type1,
                WebhookEndpointPausedByType3Type1]): platform: nothing was delivered for the platform's pause period while
                events failed
            delivered (int): Events delivered since the endpoint was made
            last_delivered_at (Union[None, datetime.datetime]):
            last_failed_at (Union[None, datetime.datetime]):
            retrying (int): Failed events still being tried
            dead (int): Events whose last try failed, kept for a limited number of days
            cursor (Union[None, str]): The last event of the stream handed on: what a resume continues from
            previous_secret_until (Union[None, datetime.datetime]): After a rotation, until when the previous secret also
                signs
            created_at (datetime.datetime):
    """

    id: UUID
    url: str
    event_types: list[str]
    description: Union[None, str]
    status: WebhookEndpointStatus
    paused_reason: Union[None, str]
    paused_by: Union[
        None,
        WebhookEndpointPausedByType1,
        WebhookEndpointPausedByType2Type1,
        WebhookEndpointPausedByType3Type1,
    ]
    delivered: int
    last_delivered_at: Union[None, datetime.datetime]
    last_failed_at: Union[None, datetime.datetime]
    retrying: int
    dead: int
    cursor: Union[None, str]
    previous_secret_until: Union[None, datetime.datetime]
    created_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        url = self.url

        event_types = self.event_types

        description: Union[None, str]
        description = self.description

        status = self.status.value

        paused_reason: Union[None, str]
        paused_reason = self.paused_reason

        paused_by: Union[None, str]
        if isinstance(self.paused_by, WebhookEndpointPausedByType1):
            paused_by = self.paused_by.value
        elif isinstance(self.paused_by, WebhookEndpointPausedByType2Type1):
            paused_by = self.paused_by.value
        elif isinstance(self.paused_by, WebhookEndpointPausedByType3Type1):
            paused_by = self.paused_by.value
        else:
            paused_by = self.paused_by

        delivered = self.delivered

        last_delivered_at: Union[None, str]
        if isinstance(self.last_delivered_at, datetime.datetime):
            last_delivered_at = self.last_delivered_at.isoformat()
        else:
            last_delivered_at = self.last_delivered_at

        last_failed_at: Union[None, str]
        if isinstance(self.last_failed_at, datetime.datetime):
            last_failed_at = self.last_failed_at.isoformat()
        else:
            last_failed_at = self.last_failed_at

        retrying = self.retrying

        dead = self.dead

        cursor: Union[None, str]
        cursor = self.cursor

        previous_secret_until: Union[None, str]
        if isinstance(self.previous_secret_until, datetime.datetime):
            previous_secret_until = self.previous_secret_until.isoformat()
        else:
            previous_secret_until = self.previous_secret_until

        created_at = self.created_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "url": url,
                "event_types": event_types,
                "description": description,
                "status": status,
                "paused_reason": paused_reason,
                "paused_by": paused_by,
                "delivered": delivered,
                "last_delivered_at": last_delivered_at,
                "last_failed_at": last_failed_at,
                "retrying": retrying,
                "dead": dead,
                "cursor": cursor,
                "previous_secret_until": previous_secret_until,
                "created_at": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        url = d.pop("url")

        event_types = cast(list[str], d.pop("event_types"))

        def _parse_description(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        description = _parse_description(d.pop("description"))

        status = WebhookEndpointStatus(d.pop("status"))

        def _parse_paused_reason(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        paused_reason = _parse_paused_reason(d.pop("paused_reason"))

        def _parse_paused_by(
            data: object,
        ) -> Union[
            None,
            WebhookEndpointPausedByType1,
            WebhookEndpointPausedByType2Type1,
            WebhookEndpointPausedByType3Type1,
        ]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                paused_by_type_1 = WebhookEndpointPausedByType1(data)

                return paused_by_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                paused_by_type_2_type_1 = WebhookEndpointPausedByType2Type1(data)

                return paused_by_type_2_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                paused_by_type_3_type_1 = WebhookEndpointPausedByType3Type1(data)

                return paused_by_type_3_type_1
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    None,
                    WebhookEndpointPausedByType1,
                    WebhookEndpointPausedByType2Type1,
                    WebhookEndpointPausedByType3Type1,
                ],
                data,
            )

        paused_by = _parse_paused_by(d.pop("paused_by"))

        delivered = d.pop("delivered")

        def _parse_last_delivered_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_delivered_at_type_0 = isoparse(data)

                return last_delivered_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        last_delivered_at = _parse_last_delivered_at(d.pop("last_delivered_at"))

        def _parse_last_failed_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_failed_at_type_0 = isoparse(data)

                return last_failed_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        last_failed_at = _parse_last_failed_at(d.pop("last_failed_at"))

        retrying = d.pop("retrying")

        dead = d.pop("dead")

        def _parse_cursor(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        cursor = _parse_cursor(d.pop("cursor"))

        def _parse_previous_secret_until(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                previous_secret_until_type_0 = isoparse(data)

                return previous_secret_until_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        previous_secret_until = _parse_previous_secret_until(d.pop("previous_secret_until"))

        created_at = isoparse(d.pop("created_at"))

        webhook_endpoint = cls(
            id=id,
            url=url,
            event_types=event_types,
            description=description,
            status=status,
            paused_reason=paused_reason,
            paused_by=paused_by,
            delivered=delivered,
            last_delivered_at=last_delivered_at,
            last_failed_at=last_failed_at,
            retrying=retrying,
            dead=dead,
            cursor=cursor,
            previous_secret_until=previous_secret_until,
            created_at=created_at,
        )

        webhook_endpoint.additional_properties = d
        return webhook_endpoint

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
