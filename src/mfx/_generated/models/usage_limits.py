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

T = TypeVar("T", bound="UsageLimits")


@_attrs_define
class UsageLimits:
    """The calling key's ceilings.

    Attributes:
        commands_per_s (Union[None, Unset, int]):
        md_msgs_per_s (Union[None, Unset, int]):
        ws_conns (Union[None, Unset, int]):
    """

    commands_per_s: Union[None, Unset, int] = UNSET
    md_msgs_per_s: Union[None, Unset, int] = UNSET
    ws_conns: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        commands_per_s: Union[None, Unset, int]
        if isinstance(self.commands_per_s, Unset):
            commands_per_s = UNSET
        else:
            commands_per_s = self.commands_per_s

        md_msgs_per_s: Union[None, Unset, int]
        if isinstance(self.md_msgs_per_s, Unset):
            md_msgs_per_s = UNSET
        else:
            md_msgs_per_s = self.md_msgs_per_s

        ws_conns: Union[None, Unset, int]
        if isinstance(self.ws_conns, Unset):
            ws_conns = UNSET
        else:
            ws_conns = self.ws_conns

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if commands_per_s is not UNSET:
            field_dict["commands_per_s"] = commands_per_s
        if md_msgs_per_s is not UNSET:
            field_dict["md_msgs_per_s"] = md_msgs_per_s
        if ws_conns is not UNSET:
            field_dict["ws_conns"] = ws_conns

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_commands_per_s(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        commands_per_s = _parse_commands_per_s(d.pop("commands_per_s", UNSET))

        def _parse_md_msgs_per_s(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        md_msgs_per_s = _parse_md_msgs_per_s(d.pop("md_msgs_per_s", UNSET))

        def _parse_ws_conns(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        ws_conns = _parse_ws_conns(d.pop("ws_conns", UNSET))

        usage_limits = cls(
            commands_per_s=commands_per_s,
            md_msgs_per_s=md_msgs_per_s,
            ws_conns=ws_conns,
        )

        usage_limits.additional_properties = d
        return usage_limits

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
