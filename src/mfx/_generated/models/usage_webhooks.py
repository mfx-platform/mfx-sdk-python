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

if TYPE_CHECKING:
    from ..models.usage_webhooks_endpoints import UsageWebhooksEndpoints


T = TypeVar("T", bound="UsageWebhooks")


@_attrs_define
class UsageWebhooks:
    """
    Attributes:
        endpoints (UsageWebhooksEndpoints):
        timeout_ms (int):
        retry_after_seconds (list[int]): The waits before each retry of a failed delivery
        pause_after_hours (int):
        failure_days (int):
        in_flight_per_endpoint (int):
    """

    endpoints: "UsageWebhooksEndpoints"
    timeout_ms: int
    retry_after_seconds: list[int]
    pause_after_hours: int
    failure_days: int
    in_flight_per_endpoint: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.usage_webhooks_endpoints import UsageWebhooksEndpoints

        endpoints = self.endpoints.to_dict()

        timeout_ms = self.timeout_ms

        retry_after_seconds = self.retry_after_seconds

        pause_after_hours = self.pause_after_hours

        failure_days = self.failure_days

        in_flight_per_endpoint = self.in_flight_per_endpoint

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "endpoints": endpoints,
                "timeout_ms": timeout_ms,
                "retry_after_seconds": retry_after_seconds,
                "pause_after_hours": pause_after_hours,
                "failure_days": failure_days,
                "in_flight_per_endpoint": in_flight_per_endpoint,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.usage_webhooks_endpoints import UsageWebhooksEndpoints

        d = dict(src_dict)
        endpoints = UsageWebhooksEndpoints.from_dict(d.pop("endpoints"))

        timeout_ms = d.pop("timeout_ms")

        retry_after_seconds = cast(list[int], d.pop("retry_after_seconds"))

        pause_after_hours = d.pop("pause_after_hours")

        failure_days = d.pop("failure_days")

        in_flight_per_endpoint = d.pop("in_flight_per_endpoint")

        usage_webhooks = cls(
            endpoints=endpoints,
            timeout_ms=timeout_ms,
            retry_after_seconds=retry_after_seconds,
            pause_after_hours=pause_after_hours,
            failure_days=failure_days,
            in_flight_per_endpoint=in_flight_per_endpoint,
        )

        usage_webhooks.additional_properties = d
        return usage_webhooks

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
