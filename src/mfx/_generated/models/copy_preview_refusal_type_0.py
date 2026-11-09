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

T = TypeVar("T", bound="CopyPreviewRefusalType0")


@_attrs_define
class CopyPreviewRefusalType0:
    """Why the follow itself would be refused, as creating it would answer; null when it would be accepted

    Attributes:
        reason (str): not_on_this_venue, follows_itself, not_admitted or needs_leader_account
        options (list[str]): not_on_this_venue: the options the venue cannot honour
    """

    reason: str
    options: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        reason = self.reason

        options = self.options

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "reason": reason,
                "options": options,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        reason = d.pop("reason")

        options = cast(list[str], d.pop("options"))

        copy_preview_refusal_type_0 = cls(
            reason=reason,
            options=options,
        )

        copy_preview_refusal_type_0.additional_properties = d
        return copy_preview_refusal_type_0

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
