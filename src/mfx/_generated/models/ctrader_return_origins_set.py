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

T = TypeVar("T", bound="CtraderReturnOriginsSet")


@_attrs_define
class CtraderReturnOriginsSet:
    """
    Attributes:
        origins (list[str]):
    """

    origins: list[str]

    def to_dict(self) -> dict[str, Any]:
        origins = self.origins

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "origins": origins,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        origins = cast(list[str], d.pop("origins"))

        ctrader_return_origins_set = cls(
            origins=origins,
        )

        return ctrader_return_origins_set
