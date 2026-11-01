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

if TYPE_CHECKING:
    from ..models.expert_advisor_parameters_put_params import (
        ExpertAdvisorParametersPutParams,
    )


T = TypeVar("T", bound="ExpertAdvisorParametersPut")


@_attrs_define
class ExpertAdvisorParametersPut:
    """A parameter set for the terminal's EA. Your keys go in `params`; the platform writes them, with `enabled` and the
    version it assigns, to the EA's parameter file (`MQL5/Files/mfx/params.json`), so they never collide with the
    platform's own keys.

        Attributes:
            enabled (bool): False asks your EA to stop trading (a soft pause): it is honoured by the EA, and the hard stop
                stays the platform's
            params (ExpertAdvisorParametersPutParams): Your EA's settings, any JSON object. With the platform's keys the
                file is at most 256 KiB and 32 levels deep; no key anywhere may be named like a credential (password, secret,
                token, api key, private key, login)
    """

    enabled: bool
    params: "ExpertAdvisorParametersPutParams"

    def to_dict(self) -> dict[str, Any]:
        from ..models.expert_advisor_parameters_put_params import (
            ExpertAdvisorParametersPutParams,
        )

        enabled = self.enabled

        params = self.params.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "enabled": enabled,
                "params": params,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.expert_advisor_parameters_put_params import (
            ExpertAdvisorParametersPutParams,
        )

        d = dict(src_dict)
        enabled = d.pop("enabled")

        params = ExpertAdvisorParametersPutParams.from_dict(d.pop("params"))

        expert_advisor_parameters_put = cls(
            enabled=enabled,
            params=params,
        )

        return expert_advisor_parameters_put
