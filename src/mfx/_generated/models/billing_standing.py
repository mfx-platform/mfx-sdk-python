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

from ..models.billing_standing_cause_type_1 import BillingStandingCauseType1
from ..models.billing_standing_cause_type_2_type_1 import BillingStandingCauseType2Type1
from ..models.billing_standing_cause_type_3_type_1 import BillingStandingCauseType3Type1
from ..models.billing_standing_stage import BillingStandingStage
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.billing_action import BillingAction
    from ..models.billing_affects import BillingAffects
    from ..models.billing_standing_planned_item import BillingStandingPlannedItem


T = TypeVar("T", bound="BillingStanding")


@_attrs_define
class BillingStanding:
    """Where a billing profile stands on payment. `ok`: nothing is due. `notice`: a prepaid balance will last fewer days
    than the notice setting, or an invoice is due within it. `reminder`: the balance is used up or the invoice is past
    due; `suspends_at` is the first suspended moment and `pay_by` the last moment a payment avoids it, and requests that
    add something billed are refused with 402 `billing_payment_required`. `suspended`: the profile's MT5 terminals are
    disabled and its cTrader connections stopped, nothing deleted, and suspended days are not billed. Paying releases
    them.

        Attributes:
            stage (BillingStandingStage):
            cause (Union[BillingStandingCauseType1, BillingStandingCauseType2Type1, BillingStandingCauseType3Type1, None]):
                Null when the stage is ok
            since (Union[None, datetime.datetime]): When the stage began; null when ok
            suspends_at (Union[None, datetime.datetime]): From the reminder: the first suspended moment; null otherwise
            pay_by (Union[None, datetime.datetime]): From the reminder: the last moment a payment avoids the suspension;
                null otherwise
            action (Union['BillingAction', None]):
            held_until (Union[None, Unset, datetime.datetime]): MFX Hub has held the suspension until then; null when not
                held
            covers_days (Union[None, Unset, int]): Prepaid: whole days the balance covers at today's daily charge
            invoice_id (Union[None, UUID, Unset]): The invoice the notice or reminder is about
            affects (Union['BillingAffects', None, Unset]):
            planned (Union[Unset, list['BillingStandingPlannedItem']]): While the stage is ok or notice: the steps still to
                come if nothing is paid (the first notice, the reminder and the suspension), each dated from the settings
                billing.notice.invoice_due_days, billing.notice.low_credit_days, billing.reminder.after_due_days and
                billing.suspend.cooldown_days.<plan>. A step already reached is left out; empty when nothing is due and the
                balance outlasts the forecast. Absent from the reminder on, where suspends_at and pay_by say it. A held
                suspension (held_until) moves the suspension step.
    """

    stage: BillingStandingStage
    cause: Union[
        BillingStandingCauseType1,
        BillingStandingCauseType2Type1,
        BillingStandingCauseType3Type1,
        None,
    ]
    since: Union[None, datetime.datetime]
    suspends_at: Union[None, datetime.datetime]
    pay_by: Union[None, datetime.datetime]
    action: Union["BillingAction", None]
    held_until: Union[None, Unset, datetime.datetime] = UNSET
    covers_days: Union[None, Unset, int] = UNSET
    invoice_id: Union[None, UUID, Unset] = UNSET
    affects: Union["BillingAffects", None, Unset] = UNSET
    planned: Union[Unset, list["BillingStandingPlannedItem"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.billing_action import BillingAction
        from ..models.billing_affects import BillingAffects
        from ..models.billing_standing_planned_item import BillingStandingPlannedItem

        stage = self.stage.value

        cause: Union[None, str]
        if isinstance(self.cause, BillingStandingCauseType1):
            cause = self.cause.value
        elif isinstance(self.cause, BillingStandingCauseType2Type1):
            cause = self.cause.value
        elif isinstance(self.cause, BillingStandingCauseType3Type1):
            cause = self.cause.value
        else:
            cause = self.cause

        since: Union[None, str]
        if isinstance(self.since, datetime.datetime):
            since = self.since.isoformat()
        else:
            since = self.since

        suspends_at: Union[None, str]
        if isinstance(self.suspends_at, datetime.datetime):
            suspends_at = self.suspends_at.isoformat()
        else:
            suspends_at = self.suspends_at

        pay_by: Union[None, str]
        if isinstance(self.pay_by, datetime.datetime):
            pay_by = self.pay_by.isoformat()
        else:
            pay_by = self.pay_by

        action: Union[None, dict[str, Any]]
        if isinstance(self.action, BillingAction):
            action = self.action.to_dict()
        else:
            action = self.action

        held_until: Union[None, Unset, str]
        if isinstance(self.held_until, Unset):
            held_until = UNSET
        elif isinstance(self.held_until, datetime.datetime):
            held_until = self.held_until.isoformat()
        else:
            held_until = self.held_until

        covers_days: Union[None, Unset, int]
        if isinstance(self.covers_days, Unset):
            covers_days = UNSET
        else:
            covers_days = self.covers_days

        invoice_id: Union[None, Unset, str]
        if isinstance(self.invoice_id, Unset):
            invoice_id = UNSET
        elif isinstance(self.invoice_id, UUID):
            invoice_id = str(self.invoice_id)
        else:
            invoice_id = self.invoice_id

        affects: Union[None, Unset, dict[str, Any]]
        if isinstance(self.affects, Unset):
            affects = UNSET
        elif isinstance(self.affects, BillingAffects):
            affects = self.affects.to_dict()
        else:
            affects = self.affects

        planned: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.planned, Unset):
            planned = []
            for planned_item_data in self.planned:
                planned_item = planned_item_data.to_dict()
                planned.append(planned_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "stage": stage,
                "cause": cause,
                "since": since,
                "suspends_at": suspends_at,
                "pay_by": pay_by,
                "action": action,
            }
        )
        if held_until is not UNSET:
            field_dict["held_until"] = held_until
        if covers_days is not UNSET:
            field_dict["covers_days"] = covers_days
        if invoice_id is not UNSET:
            field_dict["invoice_id"] = invoice_id
        if affects is not UNSET:
            field_dict["affects"] = affects
        if planned is not UNSET:
            field_dict["planned"] = planned

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.billing_action import BillingAction
        from ..models.billing_affects import BillingAffects
        from ..models.billing_standing_planned_item import BillingStandingPlannedItem

        d = dict(src_dict)
        stage = BillingStandingStage._read(d.pop("stage"))

        def _parse_cause(
            data: object,
        ) -> Union[
            BillingStandingCauseType1,
            BillingStandingCauseType2Type1,
            BillingStandingCauseType3Type1,
            None,
        ]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                cause_type_1 = BillingStandingCauseType1._read(data)

                return cause_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                cause_type_2_type_1 = BillingStandingCauseType2Type1._read(data)

                return cause_type_2_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                cause_type_3_type_1 = BillingStandingCauseType3Type1._read(data)

                return cause_type_3_type_1
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    BillingStandingCauseType1,
                    BillingStandingCauseType2Type1,
                    BillingStandingCauseType3Type1,
                    None,
                ],
                data,
            )

        cause = _parse_cause(d.pop("cause"))

        def _parse_since(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                since_type_0 = isoparse(data)

                return since_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        since = _parse_since(d.pop("since"))

        def _parse_suspends_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                suspends_at_type_0 = isoparse(data)

                return suspends_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        suspends_at = _parse_suspends_at(d.pop("suspends_at"))

        def _parse_pay_by(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                pay_by_type_0 = isoparse(data)

                return pay_by_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        pay_by = _parse_pay_by(d.pop("pay_by"))

        def _parse_action(data: object) -> Union["BillingAction", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                action_type_0 = BillingAction.from_dict(data)

                return action_type_0
            except:  # noqa: E722
                pass
            return cast(Union["BillingAction", None], data)

        action = _parse_action(d.pop("action"))

        def _parse_held_until(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                held_until_type_0 = isoparse(data)

                return held_until_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        held_until = _parse_held_until(d.pop("held_until", UNSET))

        def _parse_covers_days(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        covers_days = _parse_covers_days(d.pop("covers_days", UNSET))

        def _parse_invoice_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                invoice_id_type_0 = UUID(data)

                return invoice_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        invoice_id = _parse_invoice_id(d.pop("invoice_id", UNSET))

        def _parse_affects(data: object) -> Union["BillingAffects", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                affects_type_0 = BillingAffects.from_dict(data)

                return affects_type_0
            except:  # noqa: E722
                pass
            return cast(Union["BillingAffects", None, Unset], data)

        affects = _parse_affects(d.pop("affects", UNSET))

        planned = []
        _planned = d.pop("planned", UNSET)
        for planned_item_data in _planned or []:
            planned_item = BillingStandingPlannedItem.from_dict(planned_item_data)

            planned.append(planned_item)

        billing_standing = cls(
            stage=stage,
            cause=cause,
            since=since,
            suspends_at=suspends_at,
            pay_by=pay_by,
            action=action,
            held_until=held_until,
            covers_days=covers_days,
            invoice_id=invoice_id,
            affects=affects,
            planned=planned,
        )

        billing_standing.additional_properties = d
        return billing_standing

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
