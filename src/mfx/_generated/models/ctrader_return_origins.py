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

T = TypeVar("T", bound="CtraderReturnOrigins")


@_attrs_define
class CtraderReturnOrigins:
    """
    Attributes:
        origins (list[str]): Each host lower-cased, :443 dropped, no duplicates, sorted
        enforced (bool): true when a grant's return_url is checked against origins
    """

    origins: list[str]
    enforced: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        origins = self.origins

        enforced = self.enforced

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "origins": origins,
                "enforced": enforced,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        origins = cast(list[str], d.pop("origins"))

        enforced = d.pop("enforced")

        ctrader_return_origins = cls(
            origins=origins,
            enforced=enforced,
        )

        ctrader_return_origins.additional_properties = d
        return ctrader_return_origins

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
