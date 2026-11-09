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

T = TypeVar("T", bound="CopyLogPageStats")


@_attrs_define
class CopyLogPageStats:
    """Over every row the filters and the window match, not this page

    Attributes:
        copies (int):
        filled (int):
        refused (int):
        skipped (int):
        stopout (int):
        mfx_ms_p50 (Union[None, float]): Null when no row has the stages
        mfx_ms_p99 (Union[None, float]):
        signal_to_order_ms_p50 (Union[None, float]):
        broker_ms_p50 (Union[None, float]):
    """

    copies: int
    filled: int
    refused: int
    skipped: int
    stopout: int
    mfx_ms_p50: Union[None, float]
    mfx_ms_p99: Union[None, float]
    signal_to_order_ms_p50: Union[None, float]
    broker_ms_p50: Union[None, float]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        copies = self.copies

        filled = self.filled

        refused = self.refused

        skipped = self.skipped

        stopout = self.stopout

        mfx_ms_p50: Union[None, float]
        mfx_ms_p50 = self.mfx_ms_p50

        mfx_ms_p99: Union[None, float]
        mfx_ms_p99 = self.mfx_ms_p99

        signal_to_order_ms_p50: Union[None, float]
        signal_to_order_ms_p50 = self.signal_to_order_ms_p50

        broker_ms_p50: Union[None, float]
        broker_ms_p50 = self.broker_ms_p50

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "copies": copies,
                "filled": filled,
                "refused": refused,
                "skipped": skipped,
                "stopout": stopout,
                "mfx_ms_p50": mfx_ms_p50,
                "mfx_ms_p99": mfx_ms_p99,
                "signal_to_order_ms_p50": signal_to_order_ms_p50,
                "broker_ms_p50": broker_ms_p50,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        copies = d.pop("copies")

        filled = d.pop("filled")

        refused = d.pop("refused")

        skipped = d.pop("skipped")

        stopout = d.pop("stopout")

        def _parse_mfx_ms_p50(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        mfx_ms_p50 = _parse_mfx_ms_p50(d.pop("mfx_ms_p50"))

        def _parse_mfx_ms_p99(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        mfx_ms_p99 = _parse_mfx_ms_p99(d.pop("mfx_ms_p99"))

        def _parse_signal_to_order_ms_p50(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        signal_to_order_ms_p50 = _parse_signal_to_order_ms_p50(d.pop("signal_to_order_ms_p50"))

        def _parse_broker_ms_p50(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        broker_ms_p50 = _parse_broker_ms_p50(d.pop("broker_ms_p50"))

        copy_log_page_stats = cls(
            copies=copies,
            filled=filled,
            refused=refused,
            skipped=skipped,
            stopout=stopout,
            mfx_ms_p50=mfx_ms_p50,
            mfx_ms_p99=mfx_ms_p99,
            signal_to_order_ms_p50=signal_to_order_ms_p50,
            broker_ms_p50=broker_ms_p50,
        )

        copy_log_page_stats.additional_properties = d
        return copy_log_page_stats

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
