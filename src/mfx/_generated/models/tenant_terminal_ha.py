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

from ..models.tenant_terminal_ha_fallback_state import TenantTerminalHaFallbackState
from ..models.tenant_terminal_ha_mode_type_1 import TenantTerminalHaModeType1
from ..models.tenant_terminal_ha_mode_type_2_type_1 import (
    TenantTerminalHaModeType2Type1,
)
from ..models.tenant_terminal_ha_mode_type_3_type_1 import (
    TenantTerminalHaModeType3Type1,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="TenantTerminalHa")


@_attrs_define
class TenantTerminalHa:
    """This terminal's MFX Hub HA. `enabled: false`, `mode: null` and `fallback_state: off` when HA is not on

    Attributes:
        enabled (bool):
        mode (Union[None, TenantTerminalHaModeType1, TenantTerminalHaModeType2Type1, TenantTerminalHaModeType3Type1]):
            The mode in effect; null when HA is off
        fallback_state (TenantTerminalHaFallbackState): Where the second terminal stands. off: HA is not on. starting:
            it is being created, placed or logged in. ready: it is logged in and healthy. waiting_for_capacity: there is no
            separate hardware in the farm to place it on yet. repairing: it exists and is not healthy (offline, failed,
            degraded or being moved).
    """

    enabled: bool
    mode: Union[
        None,
        TenantTerminalHaModeType1,
        TenantTerminalHaModeType2Type1,
        TenantTerminalHaModeType3Type1,
    ]
    fallback_state: TenantTerminalHaFallbackState
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled

        mode: Union[None, str]
        if isinstance(self.mode, TenantTerminalHaModeType1):
            mode = self.mode.value
        elif isinstance(self.mode, TenantTerminalHaModeType2Type1):
            mode = self.mode.value
        elif isinstance(self.mode, TenantTerminalHaModeType3Type1):
            mode = self.mode.value
        else:
            mode = self.mode

        fallback_state = self.fallback_state.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "enabled": enabled,
                "mode": mode,
                "fallback_state": fallback_state,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        enabled = d.pop("enabled")

        def _parse_mode(
            data: object,
        ) -> Union[
            None,
            TenantTerminalHaModeType1,
            TenantTerminalHaModeType2Type1,
            TenantTerminalHaModeType3Type1,
        ]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                mode_type_1 = TenantTerminalHaModeType1(data)

                return mode_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                mode_type_2_type_1 = TenantTerminalHaModeType2Type1(data)

                return mode_type_2_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                mode_type_3_type_1 = TenantTerminalHaModeType3Type1(data)

                return mode_type_3_type_1
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    None,
                    TenantTerminalHaModeType1,
                    TenantTerminalHaModeType2Type1,
                    TenantTerminalHaModeType3Type1,
                ],
                data,
            )

        mode = _parse_mode(d.pop("mode"))

        fallback_state = TenantTerminalHaFallbackState(d.pop("fallback_state"))

        tenant_terminal_ha = cls(
            enabled=enabled,
            mode=mode,
            fallback_state=fallback_state,
        )

        tenant_terminal_ha.additional_properties = d
        return tenant_terminal_ha

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
