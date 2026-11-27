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

from ..types import UNSET, Unset

T = TypeVar("T", bound="BillingAutomaticTopUp")


@_attrs_define
class BillingAutomaticTopUp:
    """
    Attributes:
        enabled (bool):
        level_usd (str): US dollars as a decimal string, signed where money leaves a balance, e.g. "-0.250000". Exact to
            six decimal places in the API. Display rule: two places on tiles and totals, four on a per-day rate in a table;
            never rounded before it is summed.
        amount_usd (str): US dollars as a decimal string, signed where money leaves a balance, e.g. "-0.250000". Exact
            to six decimal places in the API. Display rule: two places on tiles and totals, four on a per-day rate in a
            table; never rounded before it is summed.
        charged_to (Union[None, Unset, str]): Portal only: which card, then the backup
        next_expected_on (Union[None, Unset, datetime.date]):
    """

    enabled: bool
    level_usd: str
    amount_usd: str
    charged_to: Union[None, Unset, str] = UNSET
    next_expected_on: Union[None, Unset, datetime.date] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled

        level_usd = self.level_usd

        amount_usd = self.amount_usd

        charged_to: Union[None, Unset, str]
        if isinstance(self.charged_to, Unset):
            charged_to = UNSET
        else:
            charged_to = self.charged_to

        next_expected_on: Union[None, Unset, str]
        if isinstance(self.next_expected_on, Unset):
            next_expected_on = UNSET
        elif isinstance(self.next_expected_on, datetime.date):
            next_expected_on = self.next_expected_on.isoformat()
        else:
            next_expected_on = self.next_expected_on

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "enabled": enabled,
                "level_usd": level_usd,
                "amount_usd": amount_usd,
            }
        )
        if charged_to is not UNSET:
            field_dict["charged_to"] = charged_to
        if next_expected_on is not UNSET:
            field_dict["next_expected_on"] = next_expected_on

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        enabled = d.pop("enabled")

        level_usd = d.pop("level_usd")

        amount_usd = d.pop("amount_usd")

        def _parse_charged_to(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        charged_to = _parse_charged_to(d.pop("charged_to", UNSET))

        def _parse_next_expected_on(data: object) -> Union[None, Unset, datetime.date]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                next_expected_on_type_0 = isoparse(data).date()

                return next_expected_on_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.date], data)

        next_expected_on = _parse_next_expected_on(d.pop("next_expected_on", UNSET))

        billing_automatic_top_up = cls(
            enabled=enabled,
            level_usd=level_usd,
            amount_usd=amount_usd,
            charged_to=charged_to,
            next_expected_on=next_expected_on,
        )

        billing_automatic_top_up.additional_properties = d
        return billing_automatic_top_up

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
