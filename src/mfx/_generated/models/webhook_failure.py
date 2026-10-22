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

from ..models.webhook_failure_state import WebhookFailureState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.webhook_attempt import WebhookAttempt


T = TypeVar("T", bound="WebhookFailure")


@_attrs_define
class WebhookFailure:
    """One event that did not arrive at the first try, with every attempt made on it. Kept for a limited number of days

    Attributes:
        id (UUID):
        event_id (str): The event's cursor in the tenant's stream: MFX-Event-Id
        event_type (str):
        state (WebhookFailureState):
        attempts (list['WebhookAttempt']):
        next_attempt_at (Union[None, datetime.datetime]):
        prune_at (datetime.datetime):
    """

    id: UUID
    event_id: str
    event_type: str
    state: WebhookFailureState
    attempts: list["WebhookAttempt"]
    next_attempt_at: Union[None, datetime.datetime]
    prune_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.webhook_attempt import WebhookAttempt

        id = str(self.id)

        event_id = self.event_id

        event_type = self.event_type

        state = self.state.value

        attempts = []
        for attempts_item_data in self.attempts:
            attempts_item = attempts_item_data.to_dict()
            attempts.append(attempts_item)

        next_attempt_at: Union[None, str]
        if isinstance(self.next_attempt_at, datetime.datetime):
            next_attempt_at = self.next_attempt_at.isoformat()
        else:
            next_attempt_at = self.next_attempt_at

        prune_at = self.prune_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "event_id": event_id,
                "event_type": event_type,
                "state": state,
                "attempts": attempts,
                "next_attempt_at": next_attempt_at,
                "prune_at": prune_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.webhook_attempt import WebhookAttempt

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        event_id = d.pop("event_id")

        event_type = d.pop("event_type")

        state = WebhookFailureState(d.pop("state"))

        attempts = []
        _attempts = d.pop("attempts")
        for attempts_item_data in _attempts:
            attempts_item = WebhookAttempt.from_dict(attempts_item_data)

            attempts.append(attempts_item)

        def _parse_next_attempt_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                next_attempt_at_type_0 = isoparse(data)

                return next_attempt_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        next_attempt_at = _parse_next_attempt_at(d.pop("next_attempt_at"))

        prune_at = isoparse(d.pop("prune_at"))

        webhook_failure = cls(
            id=id,
            event_id=event_id,
            event_type=event_type,
            state=state,
            attempts=attempts,
            next_attempt_at=next_attempt_at,
            prune_at=prune_at,
        )

        webhook_failure.additional_properties = d
        return webhook_failure

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
