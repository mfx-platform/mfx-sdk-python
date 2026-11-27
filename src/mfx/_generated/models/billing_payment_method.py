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

from ..models.billing_payment_method_kind import BillingPaymentMethodKind
from ..models.billing_payment_method_state import BillingPaymentMethodState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.billing_payment_method_added_by import BillingPaymentMethodAddedBy
    from ..models.billing_payment_method_profiles_item import (
        BillingPaymentMethodProfilesItem,
    )


T = TypeVar("T", bound="BillingPaymentMethod")


@_attrs_define
class BillingPaymentMethod:
    """A card. Invoice is not a payment method: it is a mode of a billing profile (`BillingProfile.mode`). A card belongs
    to the organisation and is attached to profiles, each as its primary or its backup. A setup is complete when `state`
    becomes `active`; the portal polls `GET /portal/v1/billing/payment-methods/{method_id}` after the secure field. A
    method still `pending_setup` after `billing.payment_method.pending_setup_hours` (a setting, e.g. 24) is cancelled
    with its setup at the card processor and removed. Within that window a retry of the same setup answers the same
    pending method and re-confirms the same setup, never a second one.

        Attributes:
            id (UUID):
            kind (BillingPaymentMethodKind):
            profiles (list['BillingPaymentMethodProfilesItem']): The profiles it pays for, and as what; empty when it is
                attached to none
            added_by (BillingPaymentMethodAddedBy):
            display (str): e.g. Visa ending 4242
            chargeable (bool):
            state (BillingPaymentMethodState):
            expires (Union[None, Unset, str]):
            expiring_soon (Union[Unset, bool]):
            setup_client_secret (Union[None, Unset, str]): Only in the answer that starts a setup
    """

    id: UUID
    kind: BillingPaymentMethodKind
    profiles: list["BillingPaymentMethodProfilesItem"]
    added_by: "BillingPaymentMethodAddedBy"
    display: str
    chargeable: bool
    state: BillingPaymentMethodState
    expires: Union[None, Unset, str] = UNSET
    expiring_soon: Union[Unset, bool] = UNSET
    setup_client_secret: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.billing_payment_method_added_by import BillingPaymentMethodAddedBy
        from ..models.billing_payment_method_profiles_item import (
            BillingPaymentMethodProfilesItem,
        )

        id = str(self.id)

        kind = self.kind.value

        profiles = []
        for profiles_item_data in self.profiles:
            profiles_item = profiles_item_data.to_dict()
            profiles.append(profiles_item)

        added_by = self.added_by.to_dict()

        display = self.display

        chargeable = self.chargeable

        state = self.state.value

        expires: Union[None, Unset, str]
        if isinstance(self.expires, Unset):
            expires = UNSET
        else:
            expires = self.expires

        expiring_soon = self.expiring_soon

        setup_client_secret: Union[None, Unset, str]
        if isinstance(self.setup_client_secret, Unset):
            setup_client_secret = UNSET
        else:
            setup_client_secret = self.setup_client_secret

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "kind": kind,
                "profiles": profiles,
                "added_by": added_by,
                "display": display,
                "chargeable": chargeable,
                "state": state,
            }
        )
        if expires is not UNSET:
            field_dict["expires"] = expires
        if expiring_soon is not UNSET:
            field_dict["expiring_soon"] = expiring_soon
        if setup_client_secret is not UNSET:
            field_dict["setup_client_secret"] = setup_client_secret

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.billing_payment_method_added_by import BillingPaymentMethodAddedBy
        from ..models.billing_payment_method_profiles_item import (
            BillingPaymentMethodProfilesItem,
        )

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        kind = BillingPaymentMethodKind._read(d.pop("kind"))

        profiles = []
        _profiles = d.pop("profiles")
        for profiles_item_data in _profiles:
            profiles_item = BillingPaymentMethodProfilesItem.from_dict(profiles_item_data)

            profiles.append(profiles_item)

        added_by = BillingPaymentMethodAddedBy.from_dict(d.pop("added_by"))

        display = d.pop("display")

        chargeable = d.pop("chargeable")

        state = BillingPaymentMethodState._read(d.pop("state"))

        def _parse_expires(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        expires = _parse_expires(d.pop("expires", UNSET))

        expiring_soon = d.pop("expiring_soon", UNSET)

        def _parse_setup_client_secret(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        setup_client_secret = _parse_setup_client_secret(d.pop("setup_client_secret", UNSET))

        billing_payment_method = cls(
            id=id,
            kind=kind,
            profiles=profiles,
            added_by=added_by,
            display=display,
            chargeable=chargeable,
            state=state,
            expires=expires,
            expiring_soon=expiring_soon,
            setup_client_secret=setup_client_secret,
        )

        billing_payment_method.additional_properties = d
        return billing_payment_method

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
