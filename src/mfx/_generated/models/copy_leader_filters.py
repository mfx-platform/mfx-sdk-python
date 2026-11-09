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

from ..models.copy_leader_filters_side import CopyLeaderFiltersSide
from ..types import UNSET, Unset

T = TypeVar("T", bound="CopyLeaderFilters")


@_attrs_define
class CopyLeaderFilters:
    """Which of the leader's deals are copied. Nothing set copies every deal

    Attributes:
        symbols (Union[Unset, list[str]]): Only these leader symbols; empty or absent is every symbol
        tag (Union[None, Unset, str]): Only deals whose order carries this text in its comment, or in its label where
            the venue has labels
        side (Union[Unset, CopyLeaderFiltersSide]):  Default: CopyLeaderFiltersSide.BOTH.
    """

    symbols: Union[Unset, list[str]] = UNSET
    tag: Union[None, Unset, str] = UNSET
    side: Union[Unset, CopyLeaderFiltersSide] = CopyLeaderFiltersSide.BOTH

    def to_dict(self) -> dict[str, Any]:
        symbols: Union[Unset, list[str]] = UNSET
        if not isinstance(self.symbols, Unset):
            symbols = self.symbols

        tag: Union[None, Unset, str]
        if isinstance(self.tag, Unset):
            tag = UNSET
        else:
            tag = self.tag

        side: Union[Unset, str] = UNSET
        if not isinstance(self.side, Unset):
            side = self.side.value

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if symbols is not UNSET:
            field_dict["symbols"] = symbols
        if tag is not UNSET:
            field_dict["tag"] = tag
        if side is not UNSET:
            field_dict["side"] = side

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        symbols = cast(list[str], d.pop("symbols", UNSET))

        def _parse_tag(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        tag = _parse_tag(d.pop("tag", UNSET))

        _side = d.pop("side", UNSET)
        side: Union[Unset, CopyLeaderFiltersSide]
        if isinstance(_side, Unset):
            side = UNSET
        else:
            side = CopyLeaderFiltersSide(_side)

        copy_leader_filters = cls(
            symbols=symbols,
            tag=tag,
            side=side,
        )

        return copy_leader_filters
