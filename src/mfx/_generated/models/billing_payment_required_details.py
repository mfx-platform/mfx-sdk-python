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
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.billing_payment_required_details_cause import (
    BillingPaymentRequiredDetailsCause,
)
from ..models.billing_payment_required_details_stage import (
    BillingPaymentRequiredDetailsStage,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.billing_action import BillingAction


T = TypeVar("T", bound="BillingPaymentRequiredDetails")


@_attrs_define
class BillingPaymentRequiredDetails:
    """`details` of a 402 `billing_payment_required`

    Example:
        {'tenant_id': '6f1c2a0e-1b8d-4f7a-9a51-7d0c1a2b3c4d', 'billing_profile_id':
            '0b7e5c1a-3d2f-4e6a-8b9c-1d2e3f4a5b6c', 'stage': 'reminder', 'cause': 'balance_used_up', 'since':
            '2026-11-20T00:05:00Z', 'suspends_at': '2026-11-23T00:05:00Z', 'pay_by': '2026-11-23T00:04:59Z', 'action':
            {'kind': 'top_up', 'portal_path': '/billing/top-up', 'amount_usd': '10.00', 'invoice_id': None}}

    Attributes:
        tenant_id (UUID):
        billing_profile_id (UUID): The profile the request falls under; on Standard, its one profile
        stage (BillingPaymentRequiredDetailsStage):
        cause (BillingPaymentRequiredDetailsCause):
        since (datetime.datetime):
        suspends_at (datetime.datetime): The first suspended moment
        pay_by (datetime.datetime): The last moment a payment avoids the suspension
        action (BillingAction): What the payer can do to clear the standing; null when the stage is ok
    """

    tenant_id: UUID
    billing_profile_id: UUID
    stage: BillingPaymentRequiredDetailsStage
    cause: BillingPaymentRequiredDetailsCause
    since: datetime.datetime
    suspends_at: datetime.datetime
    pay_by: datetime.datetime
    action: "BillingAction"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.billing_action import BillingAction

        tenant_id = str(self.tenant_id)

        billing_profile_id = str(self.billing_profile_id)

        stage = self.stage.value

        cause = self.cause.value

        since = self.since.isoformat()

        suspends_at = self.suspends_at.isoformat()

        pay_by = self.pay_by.isoformat()

        action = self.action.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tenant_id": tenant_id,
                "billing_profile_id": billing_profile_id,
                "stage": stage,
                "cause": cause,
                "since": since,
                "suspends_at": suspends_at,
                "pay_by": pay_by,
                "action": action,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.billing_action import BillingAction

        d = dict(src_dict)
        tenant_id = UUID(d.pop("tenant_id"))

        billing_profile_id = UUID(d.pop("billing_profile_id"))

        stage = BillingPaymentRequiredDetailsStage._read(d.pop("stage"))

        cause = BillingPaymentRequiredDetailsCause._read(d.pop("cause"))

        since = isoparse(d.pop("since"))

        suspends_at = isoparse(d.pop("suspends_at"))

        pay_by = isoparse(d.pop("pay_by"))

        action = BillingAction.from_dict(d.pop("action"))

        billing_payment_required_details = cls(
            tenant_id=tenant_id,
            billing_profile_id=billing_profile_id,
            stage=stage,
            cause=cause,
            since=since,
            suspends_at=suspends_at,
            pay_by=pay_by,
            action=action,
        )

        billing_payment_required_details.additional_properties = d
        return billing_payment_required_details

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
