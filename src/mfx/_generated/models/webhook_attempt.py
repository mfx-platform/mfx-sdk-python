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

from ..models.webhook_attempt_outcome import WebhookAttemptOutcome
from ..types import UNSET, Unset

T = TypeVar("T", bound="WebhookAttempt")


@_attrs_define
class WebhookAttempt:
    """
    Attributes:
        at (datetime.datetime):
        outcome (WebhookAttemptOutcome): status: the receiver answered, not 2xx. Never a text from the receiver's side
        status_code (Union[None, int]):
        ms (Union[None, int]):
    """

    at: datetime.datetime
    outcome: WebhookAttemptOutcome
    status_code: Union[None, int]
    ms: Union[None, int]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        at = self.at.isoformat()

        outcome = self.outcome.value

        status_code: Union[None, int]
        status_code = self.status_code

        ms: Union[None, int]
        ms = self.ms

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "at": at,
                "outcome": outcome,
                "status_code": status_code,
                "ms": ms,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        at = isoparse(d.pop("at"))

        outcome = WebhookAttemptOutcome(d.pop("outcome"))

        def _parse_status_code(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        status_code = _parse_status_code(d.pop("status_code"))

        def _parse_ms(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        ms = _parse_ms(d.pop("ms"))

        webhook_attempt = cls(
            at=at,
            outcome=outcome,
            status_code=status_code,
            ms=ms,
        )

        webhook_attempt.additional_properties = d
        return webhook_attempt

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
