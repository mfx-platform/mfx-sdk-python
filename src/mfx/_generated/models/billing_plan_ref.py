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

if TYPE_CHECKING:
    from ..models.billing_agreement_ref import BillingAgreementRef


T = TypeVar("T", bound="BillingPlanRef")


@_attrs_define
class BillingPlanRef:
    """The plan the organisation is on and the prices it pays. An Enterprise organisation with an agreement in force pays
    the agreement's prices (`contract_rate_card` true) and `agreement` names it; otherwise it pays the list version in
    force.

        Attributes:
            key (str): e.g. standard or enterprise
            name (str):
            rate_card_version (str):
            contract_rate_card (bool): True when the organisation pays its own agreement's prices, not the list
            agreement (Union['BillingAgreementRef', None, Unset]): The agreement in force; null when none is, always on
                Standard
    """

    key: str
    name: str
    rate_card_version: str
    contract_rate_card: bool
    agreement: Union["BillingAgreementRef", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.billing_agreement_ref import BillingAgreementRef

        key = self.key

        name = self.name

        rate_card_version = self.rate_card_version

        contract_rate_card = self.contract_rate_card

        agreement: Union[None, Unset, dict[str, Any]]
        if isinstance(self.agreement, Unset):
            agreement = UNSET
        elif isinstance(self.agreement, BillingAgreementRef):
            agreement = self.agreement.to_dict()
        else:
            agreement = self.agreement

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key": key,
                "name": name,
                "rate_card_version": rate_card_version,
                "contract_rate_card": contract_rate_card,
            }
        )
        if agreement is not UNSET:
            field_dict["agreement"] = agreement

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.billing_agreement_ref import BillingAgreementRef

        d = dict(src_dict)
        key = d.pop("key")

        name = d.pop("name")

        rate_card_version = d.pop("rate_card_version")

        contract_rate_card = d.pop("contract_rate_card")

        def _parse_agreement(data: object) -> Union["BillingAgreementRef", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                agreement_type_0 = BillingAgreementRef.from_dict(data)

                return agreement_type_0
            except:  # noqa: E722
                pass
            return cast(Union["BillingAgreementRef", None, Unset], data)

        agreement = _parse_agreement(d.pop("agreement", UNSET))

        billing_plan_ref = cls(
            key=key,
            name=name,
            rate_card_version=rate_card_version,
            contract_rate_card=contract_rate_card,
            agreement=agreement,
        )

        billing_plan_ref.additional_properties = d
        return billing_plan_ref

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
