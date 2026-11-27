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

T = TypeVar("T", bound="TenantServiceAgreementDocumentsItem")


@_attrs_define
class TenantServiceAgreementDocumentsItem:
    """
    Attributes:
        document (str): Which legal document. The list is open: today terms (Terms of Service), privacy (Privacy
            Statement), mt5_licence (the MetaTrader 5 licence) and one Service Agreement per plan, service_agreement_<plan>
            (service_agreement_standard, service_agreement_enterprise; a plan added later adds its own). A reader must treat
            a key it does not know as one more document, by its name, and must never fail on it.
        number (int):
        plan (Union[None, str]):
        grace_ends_at (Union[None, datetime.datetime]): Null for a plan change: it waits for acceptance instead
        held (bool):
    """

    document: str
    number: int
    plan: Union[None, str]
    grace_ends_at: Union[None, datetime.datetime]
    held: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        document = self.document

        number = self.number

        plan: Union[None, str]
        plan = self.plan

        grace_ends_at: Union[None, str]
        if isinstance(self.grace_ends_at, datetime.datetime):
            grace_ends_at = self.grace_ends_at.isoformat()
        else:
            grace_ends_at = self.grace_ends_at

        held = self.held

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "document": document,
                "number": number,
                "plan": plan,
                "grace_ends_at": grace_ends_at,
                "held": held,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        document = d.pop("document")

        number = d.pop("number")

        def _parse_plan(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        plan = _parse_plan(d.pop("plan"))

        def _parse_grace_ends_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                grace_ends_at_type_0 = isoparse(data)

                return grace_ends_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        grace_ends_at = _parse_grace_ends_at(d.pop("grace_ends_at"))

        held = d.pop("held")

        tenant_service_agreement_documents_item = cls(
            document=document,
            number=number,
            plan=plan,
            grace_ends_at=grace_ends_at,
            held=held,
        )

        tenant_service_agreement_documents_item.additional_properties = d
        return tenant_service_agreement_documents_item

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
