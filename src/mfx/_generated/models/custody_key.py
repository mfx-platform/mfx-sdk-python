from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, BinaryIO, Generator, Optional, TextIO, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CustodyKey")


@_attrs_define
class CustodyKey:
    """The state of the organisation's own key, which wraps the keys its data is encrypted with

    Attributes:
        created (bool): The key exists. It is created when the organisation becomes Enterprise
        hsm_backed (bool): The key is protected by a hardware security module
        release_policy_immutable (bool): The policy that releases the key only to an attested confidential machine
            cannot be changed, by anyone
    """

    created: bool
    hsm_backed: bool
    release_policy_immutable: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created = self.created

        hsm_backed = self.hsm_backed

        release_policy_immutable = self.release_policy_immutable

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created": created,
                "hsm_backed": hsm_backed,
                "release_policy_immutable": release_policy_immutable,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        created = d.pop("created")

        hsm_backed = d.pop("hsm_backed")

        release_policy_immutable = d.pop("release_policy_immutable")

        custody_key = cls(
            created=created,
            hsm_backed=hsm_backed,
            release_policy_immutable=release_policy_immutable,
        )

        custody_key.additional_properties = d
        return custody_key

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
