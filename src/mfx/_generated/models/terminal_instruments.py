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

T = TypeVar("T", bound="TerminalInstruments")


@_attrs_define
class TerminalInstruments:
    """The whole list, replacing the one the terminal has. Not a patch: send every instrument the terminal should watch. An
    empty list is allowed (an execution-only terminal watches nothing).

        Attributes:
            instruments (list[str]): In the broker's own names (e.g. EURUSD.sd). The farm's OS caps the count.
            depth_instruments (Union[Unset, list[str]]): The symbols of `instruments` whose market depth (order book) this
                terminal reads and streams on `book:{server_id}:{symbol}`. The whole list, like `instruments`; `[]` stops depth.
                Omitted, the terminal keeps the depth symbols it has that are still in `instruments`, so an instrument removed
                is also no longer read for depth. At most the lesser of the farm's `depth_max` and the platform's per-terminal
                cap (422 `unprocessable`, details `{depth_instruments, max}`); a farm whose `depth_max` is 0 refuses any (422
                `depth_not_offered`); a symbol that is not in `instruments` is 422 `unprocessable` (details
                `{not_instruments}`). Many brokers publish no depth for most FX symbols: asking for it costs nothing then, and
                the channel carries nothing.
    """

    instruments: list[str]
    depth_instruments: Union[Unset, list[str]] = UNSET

    def to_dict(self) -> dict[str, Any]:
        instruments = self.instruments

        depth_instruments: Union[Unset, list[str]] = UNSET
        if not isinstance(self.depth_instruments, Unset):
            depth_instruments = self.depth_instruments

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "instruments": instruments,
            }
        )
        if depth_instruments is not UNSET:
            field_dict["depth_instruments"] = depth_instruments

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        instruments = cast(list[str], d.pop("instruments"))

        depth_instruments = cast(list[str], d.pop("depth_instruments", UNSET))

        terminal_instruments = cls(
            instruments=instruments,
            depth_instruments=depth_instruments,
        )

        return terminal_instruments
