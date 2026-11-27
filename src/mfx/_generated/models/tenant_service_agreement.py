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
    from ..models.plan_change_summary import PlanChangeSummary
    from ..models.tenant_service_agreement_documents_item import (
        TenantServiceAgreementDocumentsItem,
    )


T = TypeVar("T", bound="TenantServiceAgreement")


@_attrs_define
class TenantServiceAgreement:
    """What the calling key's organisation must still accept before it can add anything

    Attributes:
        due (bool): Something is waiting to be accepted
        held (bool): Additions are refused 409 service_agreement_not_accepted (or terms_not_accepted) now
        plan (str): The plan in force
        plan_change (Union['PlanChangeSummary', None]):
        documents (list['TenantServiceAgreementDocumentsItem']):
        accept_url (str): Where an owner or admin accepts, in the customer portal
    """

    due: bool
    held: bool
    plan: str
    plan_change: Union["PlanChangeSummary", None]
    documents: list["TenantServiceAgreementDocumentsItem"]
    accept_url: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.plan_change_summary import PlanChangeSummary
        from ..models.tenant_service_agreement_documents_item import (
            TenantServiceAgreementDocumentsItem,
        )

        due = self.due

        held = self.held

        plan = self.plan

        plan_change: Union[None, dict[str, Any]]
        if isinstance(self.plan_change, PlanChangeSummary):
            plan_change = self.plan_change.to_dict()
        else:
            plan_change = self.plan_change

        documents = []
        for documents_item_data in self.documents:
            documents_item = documents_item_data.to_dict()
            documents.append(documents_item)

        accept_url = self.accept_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "due": due,
                "held": held,
                "plan": plan,
                "plan_change": plan_change,
                "documents": documents,
                "accept_url": accept_url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.plan_change_summary import PlanChangeSummary
        from ..models.tenant_service_agreement_documents_item import (
            TenantServiceAgreementDocumentsItem,
        )

        d = dict(src_dict)
        due = d.pop("due")

        held = d.pop("held")

        plan = d.pop("plan")

        def _parse_plan_change(data: object) -> Union["PlanChangeSummary", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                plan_change_type_0 = PlanChangeSummary.from_dict(data)

                return plan_change_type_0
            except:  # noqa: E722
                pass
            return cast(Union["PlanChangeSummary", None], data)

        plan_change = _parse_plan_change(d.pop("plan_change"))

        documents = []
        _documents = d.pop("documents")
        for documents_item_data in _documents:
            documents_item = TenantServiceAgreementDocumentsItem.from_dict(documents_item_data)

            documents.append(documents_item)

        accept_url = d.pop("accept_url")

        tenant_service_agreement = cls(
            due=due,
            held=held,
            plan=plan,
            plan_change=plan_change,
            documents=documents,
            accept_url=accept_url,
        )

        tenant_service_agreement.additional_properties = d
        return tenant_service_agreement

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
