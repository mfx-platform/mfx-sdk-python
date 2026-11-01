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

from ..models.terminal_ha_mode_type_1 import TerminalHaModeType1
from ..models.terminal_ha_mode_type_2_type_1 import TerminalHaModeType2Type1
from ..models.terminal_ha_mode_type_3_type_1 import TerminalHaModeType3Type1
from ..types import UNSET, Unset

T = TypeVar("T", bound="TerminalHa")


@_attrs_define
class TerminalHa:
    """MFX Hub HA for one terminal. On, MFX Hub runs a second terminal on the same broker login, on separate hardware,
    ready to take over; you keep this terminal's id for everything and never see the second one. It is not in your
    terminal quota, your usage or your terminals per login, and it is not billed while HA is not priced. It is one more
    session on the login, so the broker's limit of sessions applies.

        Attributes:
            enabled (bool):
            mode (Union[None, TerminalHaModeType1, TerminalHaModeType2Type1, TerminalHaModeType3Type1, Unset]): hot: the
                second terminal stays logged in and takes over at once. warm: it waits on reserved capacity without a broker
                session and takes over after one login; not offered yet (422 `unprocessable`). Omitted: the mode this terminal
                already has, else hot.
    """

    enabled: bool
    mode: Union[
        None, TerminalHaModeType1, TerminalHaModeType2Type1, TerminalHaModeType3Type1, Unset
    ] = UNSET

    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled

        mode: Union[None, Unset, str]
        if isinstance(self.mode, Unset):
            mode = UNSET
        elif isinstance(self.mode, TerminalHaModeType1):
            mode = self.mode.value
        elif isinstance(self.mode, TerminalHaModeType2Type1):
            mode = self.mode.value
        elif isinstance(self.mode, TerminalHaModeType3Type1):
            mode = self.mode.value
        else:
            mode = self.mode

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "enabled": enabled,
            }
        )
        if mode is not UNSET:
            field_dict["mode"] = mode

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        enabled = d.pop("enabled")

        def _parse_mode(
            data: object,
        ) -> Union[
            None, TerminalHaModeType1, TerminalHaModeType2Type1, TerminalHaModeType3Type1, Unset
        ]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                mode_type_1 = TerminalHaModeType1(data)

                return mode_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                mode_type_2_type_1 = TerminalHaModeType2Type1(data)

                return mode_type_2_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                mode_type_3_type_1 = TerminalHaModeType3Type1(data)

                return mode_type_3_type_1
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    None,
                    TerminalHaModeType1,
                    TerminalHaModeType2Type1,
                    TerminalHaModeType3Type1,
                    Unset,
                ],
                data,
            )

        mode = _parse_mode(d.pop("mode", UNSET))

        terminal_ha = cls(
            enabled=enabled,
            mode=mode,
        )

        return terminal_ha
