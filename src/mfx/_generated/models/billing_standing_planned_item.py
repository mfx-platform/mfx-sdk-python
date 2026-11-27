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

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.billing_standing_planned_item_step import BillingStandingPlannedItemStep
from ..types import UNSET, Unset

T = TypeVar("T", bound="BillingStandingPlannedItem")


@_attrs_define
class BillingStandingPlannedItem:
    """
    Attributes:
        at (datetime.datetime):
        step (BillingStandingPlannedItemStep):
        text (str): The step in words, e.g. Reminder, if unpaid: names the suspension date
    """

    at: datetime.datetime
    step: BillingStandingPlannedItemStep
    text: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        at = self.at.isoformat()

        step = self.step.value

        text = self.text

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "at": at,
                "step": step,
                "text": text,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        at = isoparse(d.pop("at"))

        step = BillingStandingPlannedItemStep._read(d.pop("step"))

        text = d.pop("text")

        billing_standing_planned_item = cls(
            at=at,
            step=step,
            text=text,
        )

        billing_standing_planned_item.additional_properties = d
        return billing_standing_planned_item

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
