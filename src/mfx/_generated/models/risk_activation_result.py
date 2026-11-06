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
    from ..models.risk_activation_result_results_item import (
        RiskActivationResultResultsItem,
    )


T = TypeVar("T", bound="RiskActivationResult")


@_attrs_define
class RiskActivationResult:
    """
    Attributes:
        results (list['RiskActivationResultResultsItem']):
    """

    results: list["RiskActivationResultResultsItem"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.risk_activation_result_results_item import (
            RiskActivationResultResultsItem,
        )

        results = []
        for results_item_data in self.results:
            results_item = results_item_data.to_dict()
            results.append(results_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "results": results,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.risk_activation_result_results_item import (
            RiskActivationResultResultsItem,
        )

        d = dict(src_dict)
        results = []
        _results = d.pop("results")
        for results_item_data in _results:
            results_item = RiskActivationResultResultsItem.from_dict(results_item_data)

            results.append(results_item)

        risk_activation_result = cls(
            results=results,
        )

        risk_activation_result.additional_properties = d
        return risk_activation_result

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
