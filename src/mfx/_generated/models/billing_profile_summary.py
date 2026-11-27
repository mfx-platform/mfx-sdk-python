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

from ..models.billing_profile_summary_at_cap import BillingProfileSummaryAtCap
from ..models.billing_profile_summary_mode import BillingProfileSummaryMode
from ..models.billing_profile_summary_mode_source import BillingProfileSummaryModeSource
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.billing_automatic_top_up import BillingAutomaticTopUp
    from ..models.billing_last_failure import BillingLastFailure
    from ..models.billing_profile_summary_covers_summary import (
        BillingProfileSummaryCoversSummary,
    )
    from ..models.billing_standing import BillingStanding


T = TypeVar("T", bound="BillingProfileSummary")


@_attrs_define
class BillingProfileSummary:
    """One billing profile as the summary shows it. Every money read below is per profile

    Attributes:
        id (UUID):
        name (str):
        mode (BillingProfileSummaryMode): How the profile pays. Invoice is a mode of the profile, not a payment method
        is_default (bool): Standard has exactly one profile, its default
        balance_usd (str): US dollars as a decimal string, signed where money leaves a balance, e.g. "-0.250000". Exact
            to six decimal places in the API. Display rule: two places on tiles and totals, four on a per-day rate in a
            table; never rounded before it is summed.
        daily_usd (str): US dollars as a decimal string, signed where money leaves a balance, e.g. "-0.250000". Exact to
            six decimal places in the API. Display rule: two places on tiles and totals, four on a per-day rate in a table;
            never rounded before it is summed.
        month_to_date_usd (str): US dollars as a decimal string, signed where money leaves a balance, e.g. "-0.250000".
            Exact to six decimal places in the API. Display rule: two places on tiles and totals, four on a per-day rate in
            a table; never rounded before it is summed.
        standing (BillingStanding): Where a billing profile stands on payment. `ok`: nothing is due. `notice`: a prepaid
            balance will last fewer days than the notice setting, or an invoice is due within it. `reminder`: the balance is
            used up or the invoice is past due; `suspends_at` is the first suspended moment and `pay_by` the last moment a
            payment avoids it, and requests that add something billed are refused with 402 `billing_payment_required`.
            `suspended`: the profile's MT5 terminals are disabled and its cTrader connections stopped, nothing deleted, and
            suspended days are not billed. Paying releases them.
        mode_source (Union[Unset, BillingProfileSummaryModeSource]): Where the mode comes from, read only. agreement: an
            agreement is in force and every profile of the organisation pays in its payment mode. plan: none is in force,
            and the mode is the one the profile was created with, within what the plan allows (Standard: prepaid). A
            profile's mode is never changed on the profile itself
        credit_usd (Union[Unset, str]): US dollars as a decimal string, signed where money leaves a balance, e.g.
            "-0.250000". Exact to six decimal places in the API. Display rule: two places on tiles and totals, four on a
            per-day rate in a table; never rounded before it is summed.
        forecast_month_usd (Union[Unset, str]): US dollars as a decimal string, signed where money leaves a balance,
            e.g. "-0.250000". Exact to six decimal places in the API. Display rule: two places on tiles and totals, four on
            a per-day rate in a table; never rounded before it is summed.
        monthly_cap_usd (Union[None, Unset, str]): Null for no cap
        cap_used_pct (Union[None, Unset, int]):
        at_cap (Union[Unset, BillingProfileSummaryAtCap]):
        automatic_top_up (Union['BillingAutomaticTopUp', None, Unset]):
        accounts (Union[Unset, int]): Accounts in the profile's scope
        covers_summary (Union[Unset, BillingProfileSummaryCoversSummary]):
        paid_by (Union[Unset, str]): How it pays, in words: e.g. Visa ending 4242, or Invoice, 30 days
        last_failure (Union['BillingLastFailure', None, Unset]):
        overdue_usd (Union[Unset, str]): US dollars as a decimal string, signed where money leaves a balance, e.g.
            "-0.250000". Exact to six decimal places in the API. Display rule: two places on tiles and totals, four on a
            per-day rate in a table; never rounded before it is summed.
    """

    id: UUID
    name: str
    mode: BillingProfileSummaryMode
    is_default: bool
    balance_usd: str
    daily_usd: str
    month_to_date_usd: str
    standing: "BillingStanding"
    mode_source: Union[Unset, BillingProfileSummaryModeSource] = UNSET
    credit_usd: Union[Unset, str] = UNSET
    forecast_month_usd: Union[Unset, str] = UNSET
    monthly_cap_usd: Union[None, Unset, str] = UNSET
    cap_used_pct: Union[None, Unset, int] = UNSET
    at_cap: Union[Unset, BillingProfileSummaryAtCap] = UNSET
    automatic_top_up: Union["BillingAutomaticTopUp", None, Unset] = UNSET
    accounts: Union[Unset, int] = UNSET
    covers_summary: Union[Unset, "BillingProfileSummaryCoversSummary"] = UNSET
    paid_by: Union[Unset, str] = UNSET
    last_failure: Union["BillingLastFailure", None, Unset] = UNSET
    overdue_usd: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.billing_automatic_top_up import BillingAutomaticTopUp
        from ..models.billing_last_failure import BillingLastFailure
        from ..models.billing_profile_summary_covers_summary import (
            BillingProfileSummaryCoversSummary,
        )
        from ..models.billing_standing import BillingStanding

        id = str(self.id)

        name = self.name

        mode = self.mode.value

        is_default = self.is_default

        balance_usd = self.balance_usd

        daily_usd = self.daily_usd

        month_to_date_usd = self.month_to_date_usd

        standing = self.standing.to_dict()

        mode_source: Union[Unset, str] = UNSET
        if not isinstance(self.mode_source, Unset):
            mode_source = self.mode_source.value

        credit_usd = self.credit_usd

        forecast_month_usd = self.forecast_month_usd

        monthly_cap_usd: Union[None, Unset, str]
        if isinstance(self.monthly_cap_usd, Unset):
            monthly_cap_usd = UNSET
        else:
            monthly_cap_usd = self.monthly_cap_usd

        cap_used_pct: Union[None, Unset, int]
        if isinstance(self.cap_used_pct, Unset):
            cap_used_pct = UNSET
        else:
            cap_used_pct = self.cap_used_pct

        at_cap: Union[Unset, str] = UNSET
        if not isinstance(self.at_cap, Unset):
            at_cap = self.at_cap.value

        automatic_top_up: Union[None, Unset, dict[str, Any]]
        if isinstance(self.automatic_top_up, Unset):
            automatic_top_up = UNSET
        elif isinstance(self.automatic_top_up, BillingAutomaticTopUp):
            automatic_top_up = self.automatic_top_up.to_dict()
        else:
            automatic_top_up = self.automatic_top_up

        accounts = self.accounts

        covers_summary: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.covers_summary, Unset):
            covers_summary = self.covers_summary.to_dict()

        paid_by = self.paid_by

        last_failure: Union[None, Unset, dict[str, Any]]
        if isinstance(self.last_failure, Unset):
            last_failure = UNSET
        elif isinstance(self.last_failure, BillingLastFailure):
            last_failure = self.last_failure.to_dict()
        else:
            last_failure = self.last_failure

        overdue_usd = self.overdue_usd

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "mode": mode,
                "is_default": is_default,
                "balance_usd": balance_usd,
                "daily_usd": daily_usd,
                "month_to_date_usd": month_to_date_usd,
                "standing": standing,
            }
        )
        if mode_source is not UNSET:
            field_dict["mode_source"] = mode_source
        if credit_usd is not UNSET:
            field_dict["credit_usd"] = credit_usd
        if forecast_month_usd is not UNSET:
            field_dict["forecast_month_usd"] = forecast_month_usd
        if monthly_cap_usd is not UNSET:
            field_dict["monthly_cap_usd"] = monthly_cap_usd
        if cap_used_pct is not UNSET:
            field_dict["cap_used_pct"] = cap_used_pct
        if at_cap is not UNSET:
            field_dict["at_cap"] = at_cap
        if automatic_top_up is not UNSET:
            field_dict["automatic_top_up"] = automatic_top_up
        if accounts is not UNSET:
            field_dict["accounts"] = accounts
        if covers_summary is not UNSET:
            field_dict["covers_summary"] = covers_summary
        if paid_by is not UNSET:
            field_dict["paid_by"] = paid_by
        if last_failure is not UNSET:
            field_dict["last_failure"] = last_failure
        if overdue_usd is not UNSET:
            field_dict["overdue_usd"] = overdue_usd

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.billing_automatic_top_up import BillingAutomaticTopUp
        from ..models.billing_last_failure import BillingLastFailure
        from ..models.billing_profile_summary_covers_summary import (
            BillingProfileSummaryCoversSummary,
        )
        from ..models.billing_standing import BillingStanding

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        name = d.pop("name")

        mode = BillingProfileSummaryMode._read(d.pop("mode"))

        is_default = d.pop("is_default")

        balance_usd = d.pop("balance_usd")

        daily_usd = d.pop("daily_usd")

        month_to_date_usd = d.pop("month_to_date_usd")

        standing = BillingStanding.from_dict(d.pop("standing"))

        _mode_source = d.pop("mode_source", UNSET)
        mode_source: Union[Unset, BillingProfileSummaryModeSource]
        if isinstance(_mode_source, Unset):
            mode_source = UNSET
        else:
            mode_source = BillingProfileSummaryModeSource._read(_mode_source)

        credit_usd = d.pop("credit_usd", UNSET)

        forecast_month_usd = d.pop("forecast_month_usd", UNSET)

        def _parse_monthly_cap_usd(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        monthly_cap_usd = _parse_monthly_cap_usd(d.pop("monthly_cap_usd", UNSET))

        def _parse_cap_used_pct(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        cap_used_pct = _parse_cap_used_pct(d.pop("cap_used_pct", UNSET))

        _at_cap = d.pop("at_cap", UNSET)
        at_cap: Union[Unset, BillingProfileSummaryAtCap]
        if isinstance(_at_cap, Unset):
            at_cap = UNSET
        else:
            at_cap = BillingProfileSummaryAtCap._read(_at_cap)

        def _parse_automatic_top_up(data: object) -> Union["BillingAutomaticTopUp", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                automatic_top_up_type_0 = BillingAutomaticTopUp.from_dict(data)

                return automatic_top_up_type_0
            except:  # noqa: E722
                pass
            return cast(Union["BillingAutomaticTopUp", None, Unset], data)

        automatic_top_up = _parse_automatic_top_up(d.pop("automatic_top_up", UNSET))

        accounts = d.pop("accounts", UNSET)

        _covers_summary = d.pop("covers_summary", UNSET)
        covers_summary: Union[Unset, BillingProfileSummaryCoversSummary]
        if isinstance(_covers_summary, Unset):
            covers_summary = UNSET
        else:
            covers_summary = BillingProfileSummaryCoversSummary.from_dict(_covers_summary)

        paid_by = d.pop("paid_by", UNSET)

        def _parse_last_failure(data: object) -> Union["BillingLastFailure", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                last_failure_type_0 = BillingLastFailure.from_dict(data)

                return last_failure_type_0
            except:  # noqa: E722
                pass
            return cast(Union["BillingLastFailure", None, Unset], data)

        last_failure = _parse_last_failure(d.pop("last_failure", UNSET))

        overdue_usd = d.pop("overdue_usd", UNSET)

        billing_profile_summary = cls(
            id=id,
            name=name,
            mode=mode,
            is_default=is_default,
            balance_usd=balance_usd,
            daily_usd=daily_usd,
            month_to_date_usd=month_to_date_usd,
            standing=standing,
            mode_source=mode_source,
            credit_usd=credit_usd,
            forecast_month_usd=forecast_month_usd,
            monthly_cap_usd=monthly_cap_usd,
            cap_used_pct=cap_used_pct,
            at_cap=at_cap,
            automatic_top_up=automatic_top_up,
            accounts=accounts,
            covers_summary=covers_summary,
            paid_by=paid_by,
            last_failure=last_failure,
            overdue_usd=overdue_usd,
        )

        billing_profile_summary.additional_properties = d
        return billing_profile_summary

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
