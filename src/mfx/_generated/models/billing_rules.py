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

from ..types import UNSET, Unset

T = TypeVar("T", bound="BillingRules")


@_attrs_define
class BillingRules:
    """Portal only: the bounds a top-up, a cap and an automatic top-up take, so a field can show them

    Attributes:
        top_up_min_usd (Union[Unset, str]): US dollars as a decimal string, signed where money leaves a balance, e.g.
            "-0.250000". Exact to six decimal places in the API. Display rule: two places on tiles and totals, four on a
            per-day rate in a table; never rounded before it is summed.
        top_up_step_usd (Union[Unset, str]): US dollars as a decimal string, signed where money leaves a balance, e.g.
            "-0.250000". Exact to six decimal places in the API. Display rule: two places on tiles and totals, four on a
            per-day rate in a table; never rounded before it is summed.
        top_up_max_usd (Union[Unset, str]): US dollars as a decimal string, signed where money leaves a balance, e.g.
            "-0.250000". Exact to six decimal places in the API. Display rule: two places on tiles and totals, four on a
            per-day rate in a table; never rounded before it is summed.
        cap_min_usd (Union[Unset, str]): US dollars as a decimal string, signed where money leaves a balance, e.g.
            "-0.250000". Exact to six decimal places in the API. Display rule: two places on tiles and totals, four on a
            per-day rate in a table; never rounded before it is summed.
        cap_step_usd (Union[Unset, str]): US dollars as a decimal string, signed where money leaves a balance, e.g.
            "-0.250000". Exact to six decimal places in the API. Display rule: two places on tiles and totals, four on a
            per-day rate in a table; never rounded before it is summed.
        cap_max_usd (Union[None, Unset, str]): Null for no upper bound
        cap_warn_pct (Union[Unset, int]):
        auto_top_up_level_min_usd (Union[Unset, str]): US dollars as a decimal string, signed where money leaves a
            balance, e.g. "-0.250000". Exact to six decimal places in the API. Display rule: two places on tiles and totals,
            four on a per-day rate in a table; never rounded before it is summed.
        auto_top_up_level_step_usd (Union[Unset, str]): US dollars as a decimal string, signed where money leaves a
            balance, e.g. "-0.250000". Exact to six decimal places in the API. Display rule: two places on tiles and totals,
            four on a per-day rate in a table; never rounded before it is summed.
        auto_top_up_amount_min_usd (Union[Unset, str]): US dollars as a decimal string, signed where money leaves a
            balance, e.g. "-0.250000". Exact to six decimal places in the API. Display rule: two places on tiles and totals,
            four on a per-day rate in a table; never rounded before it is summed.
        auto_top_up_amount_step_usd (Union[Unset, str]): US dollars as a decimal string, signed where money leaves a
            balance, e.g. "-0.250000". Exact to six decimal places in the API. Display rule: two places on tiles and totals,
            four on a per-day rate in a table; never rounded before it is summed.
        low_credit_notice_days (Union[Unset, int]): A prepaid profile is in notice when its balance will last fewer than
            this many days at today's daily charge
        invoice_due_notice_days (Union[Unset, int]): An unpaid invoice puts its profile in notice this many days before
            it is due
        reminder_after_due_days (Union[Unset, int]): Days past the due date an unpaid invoice moves its profile to the
            reminder; 0 is on the due date
        cooldown_days (Union[Unset, int]): Days from the reminder to the suspension on this organisation's plan; 0 is
            the same day
    """

    top_up_min_usd: Union[Unset, str] = UNSET
    top_up_step_usd: Union[Unset, str] = UNSET
    top_up_max_usd: Union[Unset, str] = UNSET
    cap_min_usd: Union[Unset, str] = UNSET
    cap_step_usd: Union[Unset, str] = UNSET
    cap_max_usd: Union[None, Unset, str] = UNSET
    cap_warn_pct: Union[Unset, int] = UNSET
    auto_top_up_level_min_usd: Union[Unset, str] = UNSET
    auto_top_up_level_step_usd: Union[Unset, str] = UNSET
    auto_top_up_amount_min_usd: Union[Unset, str] = UNSET
    auto_top_up_amount_step_usd: Union[Unset, str] = UNSET
    low_credit_notice_days: Union[Unset, int] = UNSET
    invoice_due_notice_days: Union[Unset, int] = UNSET
    reminder_after_due_days: Union[Unset, int] = UNSET
    cooldown_days: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        top_up_min_usd = self.top_up_min_usd

        top_up_step_usd = self.top_up_step_usd

        top_up_max_usd = self.top_up_max_usd

        cap_min_usd = self.cap_min_usd

        cap_step_usd = self.cap_step_usd

        cap_max_usd: Union[None, Unset, str]
        if isinstance(self.cap_max_usd, Unset):
            cap_max_usd = UNSET
        else:
            cap_max_usd = self.cap_max_usd

        cap_warn_pct = self.cap_warn_pct

        auto_top_up_level_min_usd = self.auto_top_up_level_min_usd

        auto_top_up_level_step_usd = self.auto_top_up_level_step_usd

        auto_top_up_amount_min_usd = self.auto_top_up_amount_min_usd

        auto_top_up_amount_step_usd = self.auto_top_up_amount_step_usd

        low_credit_notice_days = self.low_credit_notice_days

        invoice_due_notice_days = self.invoice_due_notice_days

        reminder_after_due_days = self.reminder_after_due_days

        cooldown_days = self.cooldown_days

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if top_up_min_usd is not UNSET:
            field_dict["top_up_min_usd"] = top_up_min_usd
        if top_up_step_usd is not UNSET:
            field_dict["top_up_step_usd"] = top_up_step_usd
        if top_up_max_usd is not UNSET:
            field_dict["top_up_max_usd"] = top_up_max_usd
        if cap_min_usd is not UNSET:
            field_dict["cap_min_usd"] = cap_min_usd
        if cap_step_usd is not UNSET:
            field_dict["cap_step_usd"] = cap_step_usd
        if cap_max_usd is not UNSET:
            field_dict["cap_max_usd"] = cap_max_usd
        if cap_warn_pct is not UNSET:
            field_dict["cap_warn_pct"] = cap_warn_pct
        if auto_top_up_level_min_usd is not UNSET:
            field_dict["auto_top_up_level_min_usd"] = auto_top_up_level_min_usd
        if auto_top_up_level_step_usd is not UNSET:
            field_dict["auto_top_up_level_step_usd"] = auto_top_up_level_step_usd
        if auto_top_up_amount_min_usd is not UNSET:
            field_dict["auto_top_up_amount_min_usd"] = auto_top_up_amount_min_usd
        if auto_top_up_amount_step_usd is not UNSET:
            field_dict["auto_top_up_amount_step_usd"] = auto_top_up_amount_step_usd
        if low_credit_notice_days is not UNSET:
            field_dict["low_credit_notice_days"] = low_credit_notice_days
        if invoice_due_notice_days is not UNSET:
            field_dict["invoice_due_notice_days"] = invoice_due_notice_days
        if reminder_after_due_days is not UNSET:
            field_dict["reminder_after_due_days"] = reminder_after_due_days
        if cooldown_days is not UNSET:
            field_dict["cooldown_days"] = cooldown_days

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        top_up_min_usd = d.pop("top_up_min_usd", UNSET)

        top_up_step_usd = d.pop("top_up_step_usd", UNSET)

        top_up_max_usd = d.pop("top_up_max_usd", UNSET)

        cap_min_usd = d.pop("cap_min_usd", UNSET)

        cap_step_usd = d.pop("cap_step_usd", UNSET)

        def _parse_cap_max_usd(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        cap_max_usd = _parse_cap_max_usd(d.pop("cap_max_usd", UNSET))

        cap_warn_pct = d.pop("cap_warn_pct", UNSET)

        auto_top_up_level_min_usd = d.pop("auto_top_up_level_min_usd", UNSET)

        auto_top_up_level_step_usd = d.pop("auto_top_up_level_step_usd", UNSET)

        auto_top_up_amount_min_usd = d.pop("auto_top_up_amount_min_usd", UNSET)

        auto_top_up_amount_step_usd = d.pop("auto_top_up_amount_step_usd", UNSET)

        low_credit_notice_days = d.pop("low_credit_notice_days", UNSET)

        invoice_due_notice_days = d.pop("invoice_due_notice_days", UNSET)

        reminder_after_due_days = d.pop("reminder_after_due_days", UNSET)

        cooldown_days = d.pop("cooldown_days", UNSET)

        billing_rules = cls(
            top_up_min_usd=top_up_min_usd,
            top_up_step_usd=top_up_step_usd,
            top_up_max_usd=top_up_max_usd,
            cap_min_usd=cap_min_usd,
            cap_step_usd=cap_step_usd,
            cap_max_usd=cap_max_usd,
            cap_warn_pct=cap_warn_pct,
            auto_top_up_level_min_usd=auto_top_up_level_min_usd,
            auto_top_up_level_step_usd=auto_top_up_level_step_usd,
            auto_top_up_amount_min_usd=auto_top_up_amount_min_usd,
            auto_top_up_amount_step_usd=auto_top_up_amount_step_usd,
            low_credit_notice_days=low_credit_notice_days,
            invoice_due_notice_days=invoice_due_notice_days,
            reminder_after_due_days=reminder_after_due_days,
            cooldown_days=cooldown_days,
        )

        billing_rules.additional_properties = d
        return billing_rules

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
