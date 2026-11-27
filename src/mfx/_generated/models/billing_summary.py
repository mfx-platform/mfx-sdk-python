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

from ..models.billing_summary_currency import BillingSummaryCurrency
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.billing_plan_ref import BillingPlanRef
    from ..models.billing_profile_summary import BillingProfileSummary
    from ..models.billing_rules import BillingRules
    from ..models.billing_standing import BillingStanding
    from ..models.billing_summary_open_invoices import BillingSummaryOpenInvoices
    from ..models.billing_verification_ref import BillingVerificationRef


T = TypeVar("T", bound="BillingSummary")


@_attrs_define
class BillingSummary:
    """The organisation's billing: every billing profile with its standing. Standard has one, implicit profile
    (`implicit_profile` true); Enterprise may have several. `standing` at the top is the most urgent of the profiles'.
    An Enterprise organisation's agreement in force is named in `plan.agreement`.

        Example:
            {'currency': 'USD', 'plan': {'key': 'standard', 'name': 'Standard', 'rate_card_version': 'rc_v3',
                'contract_rate_card': False}, 'implicit_profile': True, 'standing': {'stage': 'notice', 'cause': 'low_balance',
                'since': '2026-11-16T00:05:00Z', 'suspends_at': None, 'pay_by': None, 'held_until': None, 'covers_days': 5,
                'invoice_id': None, 'affects': None, 'action': {'kind': 'top_up', 'portal_path': '/billing/top-up',
                'amount_usd': '10.00', 'invoice_id': None}}, 'profiles': [{'id': '0b7e5c1a-3d2f-4e6a-8b9c-1d2e3f4a5b6c', 'name':
                'Default', 'mode': 'prepaid', 'is_default': True, 'balance_usd': '9.500000', 'credit_usd': '0.000000',
                'daily_usd': '1.716667', 'month_to_date_usd': '25.85', 'forecast_month_usd': '51.60', 'monthly_cap_usd': None,
                'cap_used_pct': None, 'at_cap': 'warn_then_stop', 'automatic_top_up': None, 'accounts': 5, 'covers_summary':
                {'farms': 0, 'accounts': 5}, 'paid_by': 'Visa ending 4242', 'last_failure': None, 'standing': {'stage':
                'notice', 'cause': 'low_balance', 'since': '2026-11-16T00:05:00Z', 'suspends_at': None, 'pay_by': None,
                'held_until': None, 'covers_days': 5, 'invoice_id': None, 'affects': None, 'action': {'kind': 'top_up',
                'portal_path': '/billing/top-up', 'amount_usd': '10.00', 'invoice_id': None}}}], 'open_invoices': {'count': 0,
                'open_usd': '0.00', 'overdue_usd': '0.00'}, 'rules': {'top_up_min_usd': '10.00', 'top_up_step_usd': '5.00',
                'top_up_max_usd': '5000.00', 'cap_min_usd': '10.00', 'cap_step_usd': '5.00', 'cap_max_usd': None,
                'cap_warn_pct': 80, 'auto_top_up_level_min_usd': '5.00', 'auto_top_up_level_step_usd': '5.00',
                'auto_top_up_amount_min_usd': '10.00', 'auto_top_up_amount_step_usd': '5.00', 'low_credit_notice_days': 7,
                'invoice_due_notice_days': 7, 'reminder_after_due_days': 1, 'cooldown_days': 3}, 'verification': None}

        Attributes:
            currency (BillingSummaryCurrency):
            plan (BillingPlanRef): The plan the organisation is on and the prices it pays. An Enterprise organisation with
                an agreement in force pays the agreement's prices (`contract_rate_card` true) and `agreement` names it;
                otherwise it pays the list version in force.
            implicit_profile (bool):
            standing (BillingStanding): Where a billing profile stands on payment. `ok`: nothing is due. `notice`: a prepaid
                balance will last fewer days than the notice setting, or an invoice is due within it. `reminder`: the balance is
                used up or the invoice is past due; `suspends_at` is the first suspended moment and `pay_by` the last moment a
                payment avoids it, and requests that add something billed are refused with 402 `billing_payment_required`.
                `suspended`: the profile's MT5 terminals are disabled and its cTrader connections stopped, nothing deleted, and
                suspended days are not billed. Paying releases them.
            profiles (list['BillingProfileSummary']):
            open_invoices (BillingSummaryOpenInvoices):
            rules (Union[Unset, BillingRules]): Portal only: the bounds a top-up, a cap and an automatic top-up take, so a
                field can show them
            verification (Union['BillingVerificationRef', None, Unset]): Enterprise: where the organisation's verification
                stands, read only, for the Verified mark on Billing. The status and its documents belong to the organisation,
                not to billing; this names the status only. Null on a plan with no verification, which includes Standard.
    """

    currency: BillingSummaryCurrency
    plan: "BillingPlanRef"
    implicit_profile: bool
    standing: "BillingStanding"
    profiles: list["BillingProfileSummary"]
    open_invoices: "BillingSummaryOpenInvoices"
    rules: Union[Unset, "BillingRules"] = UNSET
    verification: Union["BillingVerificationRef", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.billing_plan_ref import BillingPlanRef
        from ..models.billing_profile_summary import BillingProfileSummary
        from ..models.billing_rules import BillingRules
        from ..models.billing_standing import BillingStanding
        from ..models.billing_summary_open_invoices import BillingSummaryOpenInvoices
        from ..models.billing_verification_ref import BillingVerificationRef

        currency = self.currency.value

        plan = self.plan.to_dict()

        implicit_profile = self.implicit_profile

        standing = self.standing.to_dict()

        profiles = []
        for profiles_item_data in self.profiles:
            profiles_item = profiles_item_data.to_dict()
            profiles.append(profiles_item)

        open_invoices = self.open_invoices.to_dict()

        rules: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.rules, Unset):
            rules = self.rules.to_dict()

        verification: Union[None, Unset, dict[str, Any]]
        if isinstance(self.verification, Unset):
            verification = UNSET
        elif isinstance(self.verification, BillingVerificationRef):
            verification = self.verification.to_dict()
        else:
            verification = self.verification

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "currency": currency,
                "plan": plan,
                "implicit_profile": implicit_profile,
                "standing": standing,
                "profiles": profiles,
                "open_invoices": open_invoices,
            }
        )
        if rules is not UNSET:
            field_dict["rules"] = rules
        if verification is not UNSET:
            field_dict["verification"] = verification

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.billing_plan_ref import BillingPlanRef
        from ..models.billing_profile_summary import BillingProfileSummary
        from ..models.billing_rules import BillingRules
        from ..models.billing_standing import BillingStanding
        from ..models.billing_summary_open_invoices import BillingSummaryOpenInvoices
        from ..models.billing_verification_ref import BillingVerificationRef

        d = dict(src_dict)
        currency = BillingSummaryCurrency._read(d.pop("currency"))

        plan = BillingPlanRef.from_dict(d.pop("plan"))

        implicit_profile = d.pop("implicit_profile")

        standing = BillingStanding.from_dict(d.pop("standing"))

        profiles = []
        _profiles = d.pop("profiles")
        for profiles_item_data in _profiles:
            profiles_item = BillingProfileSummary.from_dict(profiles_item_data)

            profiles.append(profiles_item)

        open_invoices = BillingSummaryOpenInvoices.from_dict(d.pop("open_invoices"))

        _rules = d.pop("rules", UNSET)
        rules: Union[Unset, BillingRules]
        if isinstance(_rules, Unset):
            rules = UNSET
        else:
            rules = BillingRules.from_dict(_rules)

        def _parse_verification(data: object) -> Union["BillingVerificationRef", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                verification_type_0 = BillingVerificationRef.from_dict(data)

                return verification_type_0
            except:  # noqa: E722
                pass
            return cast(Union["BillingVerificationRef", None, Unset], data)

        verification = _parse_verification(d.pop("verification", UNSET))

        billing_summary = cls(
            currency=currency,
            plan=plan,
            implicit_profile=implicit_profile,
            standing=standing,
            profiles=profiles,
            open_invoices=open_invoices,
            rules=rules,
            verification=verification,
        )

        billing_summary.additional_properties = d
        return billing_summary

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
