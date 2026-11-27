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

from ..models.billing_recipient_events_item import BillingRecipientEventsItem
from ..models.billing_recipient_kind import BillingRecipientKind
from ..types import UNSET, Unset

T = TypeVar("T", bound="BillingRecipient")


@_attrs_define
class BillingRecipient:
    """
    Attributes:
        kind (BillingRecipientKind):
        ref (str): An address, or a member's person id
        events (list[BillingRecipientEventsItem]):
    """

    kind: BillingRecipientKind
    ref: str
    events: list[BillingRecipientEventsItem]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        kind = self.kind.value

        ref = self.ref

        events = []
        for events_item_data in self.events:
            events_item = events_item_data.value
            events.append(events_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
                "ref": ref,
                "events": events,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = BillingRecipientKind._read(d.pop("kind"))

        ref = d.pop("ref")

        events = []
        _events = d.pop("events")
        for events_item_data in _events:
            events_item = BillingRecipientEventsItem._read(events_item_data)

            events.append(events_item)

        billing_recipient = cls(
            kind=kind,
            ref=ref,
            events=events,
        )

        billing_recipient.additional_properties = d
        return billing_recipient

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
