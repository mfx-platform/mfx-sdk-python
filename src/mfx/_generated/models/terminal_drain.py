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

from ..types import UNSET, Unset

T = TypeVar("T", bound="TerminalDrain")


@_attrs_define
class TerminalDrain:
    """A drain. The body is optional; omitted, the reason is recorded as not given

    Attributes:
        reason (Union[Unset, str]): Why; written to the audit log and the terminal's history
        confirm_open_positions (Union[Unset, bool]): Rule 3, as on TerminalRestart: required true when the terminal has
            open positions, or while the platform cannot tell, and only while the platform's open-position confirmation
            setting is on. Positions stay open at the broker while the terminal is drained Default: False.
    """

    reason: Union[Unset, str] = UNSET
    confirm_open_positions: Union[Unset, bool] = False

    def to_dict(self) -> dict[str, Any]:
        reason = self.reason

        confirm_open_positions = self.confirm_open_positions

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if reason is not UNSET:
            field_dict["reason"] = reason
        if confirm_open_positions is not UNSET:
            field_dict["confirm_open_positions"] = confirm_open_positions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        reason = d.pop("reason", UNSET)

        confirm_open_positions = d.pop("confirm_open_positions", UNSET)

        terminal_drain = cls(
            reason=reason,
            confirm_open_positions=confirm_open_positions,
        )

        return terminal_drain
