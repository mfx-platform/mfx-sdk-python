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

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.age import Age


T = TypeVar("T", bound="RiskAccountInputs")


@_attrs_define
class RiskAccountInputs:
    """
    Attributes:
        account_read (Age): An observation with its age. `seconds` is null when the observation is missing — which reads
            as UNKNOWN, never as zero and never as fresh (L14, L36, L43, guardrail 15).
    """

    account_read: "Age"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.age import Age

        account_read = self.account_read.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "account_read": account_read,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.age import Age

        d = dict(src_dict)
        account_read = Age.from_dict(d.pop("account_read"))

        risk_account_inputs = cls(
            account_read=account_read,
        )

        risk_account_inputs.additional_properties = d
        return risk_account_inputs

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
