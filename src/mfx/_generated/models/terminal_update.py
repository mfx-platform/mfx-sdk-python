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
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.terminal_update_refresh_ms import TerminalUpdateRefreshMs
from ..types import UNSET, Unset

T = TypeVar("T", bound="TerminalUpdate")


@_attrs_define
class TerminalUpdate:
    """What a tenant may change on a running terminal. Send only the fields to change

    Attributes:
        refresh_ms (Union[Unset, TerminalUpdateRefreshMs]): As on TerminalCreate. Applied by the cell within a minute,
            without a restart
    """

    refresh_ms: Union[Unset, TerminalUpdateRefreshMs] = UNSET

    def to_dict(self) -> dict[str, Any]:
        refresh_ms: Union[Unset, int] = UNSET
        if not isinstance(self.refresh_ms, Unset):
            refresh_ms = self.refresh_ms.value

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if refresh_ms is not UNSET:
            field_dict["refresh_ms"] = refresh_ms

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _refresh_ms = d.pop("refresh_ms", UNSET)
        refresh_ms: Union[Unset, TerminalUpdateRefreshMs]
        if isinstance(_refresh_ms, Unset):
            refresh_ms = UNSET
        else:
            refresh_ms = TerminalUpdateRefreshMs(_refresh_ms)

        terminal_update = cls(
            refresh_ms=refresh_ms,
        )

        return terminal_update
