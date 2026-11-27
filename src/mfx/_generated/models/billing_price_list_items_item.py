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

from ..models.billing_price_list_items_item_kind import BillingPriceListItemsItemKind
from ..models.billing_price_list_items_item_unit import BillingPriceListItemsItemUnit
from ..models.billing_price_list_items_item_venue_type_1 import (
    BillingPriceListItemsItemVenueType1,
)
from ..models.billing_price_list_items_item_venue_type_2_type_1 import (
    BillingPriceListItemsItemVenueType2Type1,
)
from ..models.billing_price_list_items_item_venue_type_3_type_1 import (
    BillingPriceListItemsItemVenueType3Type1,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.billing_price_list_items_item_plans import (
        BillingPriceListItemsItemPlans,
    )


T = TypeVar("T", bound="BillingPriceListItemsItem")


@_attrs_define
class BillingPriceListItemsItem:
    """
    Attributes:
        key (str):
        kind (BillingPriceListItemsItemKind):
        name (str):
        unit (BillingPriceListItemsItemUnit):
        monthly_usd (str): US dollars as a decimal string, signed where money leaves a balance, e.g. "-0.250000". Exact
            to six decimal places in the API. Display rule: two places on tiles and totals, four on a per-day rate in a
            table; never rounded before it is summed.
        plans (BillingPriceListItemsItemPlans):
        venue (Union[BillingPriceListItemsItemVenueType1, BillingPriceListItemsItemVenueType2Type1,
            BillingPriceListItemsItemVenueType3Type1, None, Unset]):
        description (Union[None, Unset, str]):
        includes (Union[Unset, list[str]]):
        provisional (Union[None, Unset, str]): Why the price may still move
        starts_on (Union[None, Unset, datetime.date]): Your agreement's prices only: the first day this price applies
        ends_on (Union[None, Unset, datetime.date]): Your agreement's prices only: the last day it applies; null to the
            end of the term
        value (Union[None, Unset, int]): Your agreement's prices only: the blocks bought, or the most accounts allowed
    """

    key: str
    kind: BillingPriceListItemsItemKind
    name: str
    unit: BillingPriceListItemsItemUnit
    monthly_usd: str
    plans: "BillingPriceListItemsItemPlans"
    venue: Union[
        BillingPriceListItemsItemVenueType1,
        BillingPriceListItemsItemVenueType2Type1,
        BillingPriceListItemsItemVenueType3Type1,
        None,
        Unset,
    ] = UNSET
    description: Union[None, Unset, str] = UNSET
    includes: Union[Unset, list[str]] = UNSET
    provisional: Union[None, Unset, str] = UNSET
    starts_on: Union[None, Unset, datetime.date] = UNSET
    ends_on: Union[None, Unset, datetime.date] = UNSET
    value: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.billing_price_list_items_item_plans import (
            BillingPriceListItemsItemPlans,
        )

        key = self.key

        kind = self.kind.value

        name = self.name

        unit = self.unit.value

        monthly_usd = self.monthly_usd

        plans = self.plans.to_dict()

        venue: Union[None, Unset, str]
        if isinstance(self.venue, Unset):
            venue = UNSET
        elif isinstance(self.venue, BillingPriceListItemsItemVenueType1):
            venue = self.venue.value
        elif isinstance(self.venue, BillingPriceListItemsItemVenueType2Type1):
            venue = self.venue.value
        elif isinstance(self.venue, BillingPriceListItemsItemVenueType3Type1):
            venue = self.venue.value
        else:
            venue = self.venue

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        includes: Union[Unset, list[str]] = UNSET
        if not isinstance(self.includes, Unset):
            includes = self.includes

        provisional: Union[None, Unset, str]
        if isinstance(self.provisional, Unset):
            provisional = UNSET
        else:
            provisional = self.provisional

        starts_on: Union[None, Unset, str]
        if isinstance(self.starts_on, Unset):
            starts_on = UNSET
        elif isinstance(self.starts_on, datetime.date):
            starts_on = self.starts_on.isoformat()
        else:
            starts_on = self.starts_on

        ends_on: Union[None, Unset, str]
        if isinstance(self.ends_on, Unset):
            ends_on = UNSET
        elif isinstance(self.ends_on, datetime.date):
            ends_on = self.ends_on.isoformat()
        else:
            ends_on = self.ends_on

        value: Union[None, Unset, int]
        if isinstance(self.value, Unset):
            value = UNSET
        else:
            value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key": key,
                "kind": kind,
                "name": name,
                "unit": unit,
                "monthly_usd": monthly_usd,
                "plans": plans,
            }
        )
        if venue is not UNSET:
            field_dict["venue"] = venue
        if description is not UNSET:
            field_dict["description"] = description
        if includes is not UNSET:
            field_dict["includes"] = includes
        if provisional is not UNSET:
            field_dict["provisional"] = provisional
        if starts_on is not UNSET:
            field_dict["starts_on"] = starts_on
        if ends_on is not UNSET:
            field_dict["ends_on"] = ends_on
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.billing_price_list_items_item_plans import (
            BillingPriceListItemsItemPlans,
        )

        d = dict(src_dict)
        key = d.pop("key")

        kind = BillingPriceListItemsItemKind._read(d.pop("kind"))

        name = d.pop("name")

        unit = BillingPriceListItemsItemUnit._read(d.pop("unit"))

        monthly_usd = d.pop("monthly_usd")

        plans = BillingPriceListItemsItemPlans.from_dict(d.pop("plans"))

        def _parse_venue(
            data: object,
        ) -> Union[
            BillingPriceListItemsItemVenueType1,
            BillingPriceListItemsItemVenueType2Type1,
            BillingPriceListItemsItemVenueType3Type1,
            None,
            Unset,
        ]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                venue_type_1 = BillingPriceListItemsItemVenueType1._read(data)

                return venue_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                venue_type_2_type_1 = BillingPriceListItemsItemVenueType2Type1._read(data)

                return venue_type_2_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                venue_type_3_type_1 = BillingPriceListItemsItemVenueType3Type1._read(data)

                return venue_type_3_type_1
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    BillingPriceListItemsItemVenueType1,
                    BillingPriceListItemsItemVenueType2Type1,
                    BillingPriceListItemsItemVenueType3Type1,
                    None,
                    Unset,
                ],
                data,
            )

        venue = _parse_venue(d.pop("venue", UNSET))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        includes = cast(list[str], d.pop("includes", UNSET))

        def _parse_provisional(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        provisional = _parse_provisional(d.pop("provisional", UNSET))

        def _parse_starts_on(data: object) -> Union[None, Unset, datetime.date]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                starts_on_type_0 = isoparse(data).date()

                return starts_on_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.date], data)

        starts_on = _parse_starts_on(d.pop("starts_on", UNSET))

        def _parse_ends_on(data: object) -> Union[None, Unset, datetime.date]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                ends_on_type_0 = isoparse(data).date()

                return ends_on_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.date], data)

        ends_on = _parse_ends_on(d.pop("ends_on", UNSET))

        def _parse_value(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        value = _parse_value(d.pop("value", UNSET))

        billing_price_list_items_item = cls(
            key=key,
            kind=kind,
            name=name,
            unit=unit,
            monthly_usd=monthly_usd,
            plans=plans,
            venue=venue,
            description=description,
            includes=includes,
            provisional=provisional,
            starts_on=starts_on,
            ends_on=ends_on,
            value=value,
        )

        billing_price_list_items_item.additional_properties = d
        return billing_price_list_items_item

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
