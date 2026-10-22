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

from ..models.usage_budget_source import UsageBudgetSource
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.usage_limits import UsageLimits
    from ..models.usage_row import UsageRow


T = TypeVar("T", bound="Usage")


@_attrs_define
class Usage:
    """What this tenant has consumed and what the calling key may still spend. The limits are the key's own, not the
    tenant's, so one runaway integration cannot starve a tenant's production traffic; `budget_source` says whether
    `budget_remaining` is a measurement or the configured allowance, exactly as the `X-MFX-Budget-Source` header does.

        Attributes:
            items (list['UsageRow']):
            limits (UsageLimits): The calling key's ceilings.
            budget_remaining (int):
            budget_source (UsageBudgetSource):
            as_of (datetime.datetime):
    """

    items: list["UsageRow"]
    limits: "UsageLimits"
    budget_remaining: int
    budget_source: UsageBudgetSource
    as_of: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.usage_limits import UsageLimits
        from ..models.usage_row import UsageRow

        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        limits = self.limits.to_dict()

        budget_remaining = self.budget_remaining

        budget_source = self.budget_source.value

        as_of = self.as_of.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "items": items,
                "limits": limits,
                "budget_remaining": budget_remaining,
                "budget_source": budget_source,
                "as_of": as_of,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.usage_limits import UsageLimits
        from ..models.usage_row import UsageRow

        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = UsageRow.from_dict(items_item_data)

            items.append(items_item)

        limits = UsageLimits.from_dict(d.pop("limits"))

        budget_remaining = d.pop("budget_remaining")

        budget_source = UsageBudgetSource(d.pop("budget_source"))

        as_of = isoparse(d.pop("as_of"))

        usage = cls(
            items=items,
            limits=limits,
            budget_remaining=budget_remaining,
            budget_source=budget_source,
            as_of=as_of,
        )

        usage.additional_properties = d
        return usage

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
