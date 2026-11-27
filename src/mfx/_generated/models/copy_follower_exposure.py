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

T = TypeVar("T", bound="CopyFollowerExposure")


@_attrs_define
class CopyFollowerExposure:
    """A follower's copied gross exposure and its share of its group's cap, in US dollars to the cent

    Attributes:
        used (str): The exposure of its open copied positions priced in USD
        share (Union[None, str]): Its signed share of its group's cap; null in no group, a group with no cap, or once
            unfollowed
    """

    used: str
    share: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        used = self.used

        share: Union[None, str]
        share = self.share

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "used": used,
                "share": share,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        used = d.pop("used")

        def _parse_share(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        share = _parse_share(d.pop("share"))

        copy_follower_exposure = cls(
            used=used,
            share=share,
        )

        copy_follower_exposure.additional_properties = d
        return copy_follower_exposure

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
