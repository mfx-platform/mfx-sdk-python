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

from ..models.risk_coverage_detector_type_1 import RiskCoverageDetectorType1
from ..models.risk_coverage_detector_type_2_type_1 import RiskCoverageDetectorType2Type1
from ..models.risk_coverage_detector_type_3_type_1 import RiskCoverageDetectorType3Type1
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.risk_coverage_kind import RiskCoverageKind


T = TypeVar("T", bound="RiskCoverage")


@_attrs_define
class RiskCoverage:
    """Per kind. A green terminal is not full coverage

    Attributes:
        monitoring (RiskCoverageKind):
        pre_trade (RiskCoverageKind):
        broker_held (RiskCoverageKind):
        managed_actions (RiskCoverageKind):
        detector (Union[None, RiskCoverageDetectorType1, RiskCoverageDetectorType2Type1,
            RiskCoverageDetectorType3Type1]): Which reads the rules are evaluated on: the cell's monitor, or the platform's
            copy of the account reads
    """

    monitoring: "RiskCoverageKind"
    pre_trade: "RiskCoverageKind"
    broker_held: "RiskCoverageKind"
    managed_actions: "RiskCoverageKind"
    detector: Union[
        None,
        RiskCoverageDetectorType1,
        RiskCoverageDetectorType2Type1,
        RiskCoverageDetectorType3Type1,
    ]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.risk_coverage_kind import RiskCoverageKind

        monitoring = self.monitoring.to_dict()

        pre_trade = self.pre_trade.to_dict()

        broker_held = self.broker_held.to_dict()

        managed_actions = self.managed_actions.to_dict()

        detector: Union[None, str]
        if isinstance(self.detector, RiskCoverageDetectorType1):
            detector = self.detector.value
        elif isinstance(self.detector, RiskCoverageDetectorType2Type1):
            detector = self.detector.value
        elif isinstance(self.detector, RiskCoverageDetectorType3Type1):
            detector = self.detector.value
        else:
            detector = self.detector

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "monitoring": monitoring,
                "pre_trade": pre_trade,
                "broker_held": broker_held,
                "managed_actions": managed_actions,
                "detector": detector,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.risk_coverage_kind import RiskCoverageKind

        d = dict(src_dict)
        monitoring = RiskCoverageKind.from_dict(d.pop("monitoring"))

        pre_trade = RiskCoverageKind.from_dict(d.pop("pre_trade"))

        broker_held = RiskCoverageKind.from_dict(d.pop("broker_held"))

        managed_actions = RiskCoverageKind.from_dict(d.pop("managed_actions"))

        def _parse_detector(
            data: object,
        ) -> Union[
            None,
            RiskCoverageDetectorType1,
            RiskCoverageDetectorType2Type1,
            RiskCoverageDetectorType3Type1,
        ]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                detector_type_1 = RiskCoverageDetectorType1(data)

                return detector_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                detector_type_2_type_1 = RiskCoverageDetectorType2Type1(data)

                return detector_type_2_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                detector_type_3_type_1 = RiskCoverageDetectorType3Type1(data)

                return detector_type_3_type_1
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    None,
                    RiskCoverageDetectorType1,
                    RiskCoverageDetectorType2Type1,
                    RiskCoverageDetectorType3Type1,
                ],
                data,
            )

        detector = _parse_detector(d.pop("detector"))

        risk_coverage = cls(
            monitoring=monitoring,
            pre_trade=pre_trade,
            broker_held=broker_held,
            managed_actions=managed_actions,
            detector=detector,
        )

        risk_coverage.additional_properties = d
        return risk_coverage

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
