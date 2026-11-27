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

from ..models.billing_action_kind import BillingActionKind
from ..types import UNSET, Unset

T = TypeVar("T", bound="BillingAction")


@_attrs_define
class BillingAction:
    """What the payer can do to clear the standing; null when the stage is ok

    Attributes:
        kind (BillingActionKind):
        portal_path (str): The portal page that does it, relative to the portal's address, e.g. /billing/top-up
        amount_usd (Union[Unset, str]): US dollars as a decimal string, signed where money leaves a balance, e.g.
            "-0.250000". Exact to six decimal places in the API. Display rule: two places on tiles and totals, four on a
            per-day rate in a table; never rounded before it is summed.
        invoice_id (Union[None, UUID, Unset]):
    """

    kind: BillingActionKind
    portal_path: str
    amount_usd: Union[Unset, str] = UNSET
    invoice_id: Union[None, UUID, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        kind = self.kind.value

        portal_path = self.portal_path

        amount_usd = self.amount_usd

        invoice_id: Union[None, Unset, str]
        if isinstance(self.invoice_id, Unset):
            invoice_id = UNSET
        elif isinstance(self.invoice_id, UUID):
            invoice_id = str(self.invoice_id)
        else:
            invoice_id = self.invoice_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
                "portal_path": portal_path,
            }
        )
        if amount_usd is not UNSET:
            field_dict["amount_usd"] = amount_usd
        if invoice_id is not UNSET:
            field_dict["invoice_id"] = invoice_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = BillingActionKind._read(d.pop("kind"))

        portal_path = d.pop("portal_path")

        amount_usd = d.pop("amount_usd", UNSET)

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

        billing_action = cls(
            kind=kind,
            portal_path=portal_path,
            amount_usd=amount_usd,
            invoice_id=invoice_id,
        )

        billing_action.additional_properties = d
        return billing_action

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
