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
    from ..models.copy_group_rollover_result_results_item_changes_additional_property import (
        CopyGroupRolloverResultResultsItemChangesAdditionalProperty,
    )


T = TypeVar("T", bound="CopyGroupRolloverResultResultsItemChanges")


@_attrs_define
class CopyGroupRolloverResultResultsItemChanges:
    """Each field changed, with its from and to; empty unless changed"""

    additional_properties: dict[
        str, "CopyGroupRolloverResultResultsItemChangesAdditionalProperty"
    ] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.copy_group_rollover_result_results_item_changes_additional_property import (
            CopyGroupRolloverResultResultsItemChangesAdditionalProperty,
        )

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.copy_group_rollover_result_results_item_changes_additional_property import (
            CopyGroupRolloverResultResultsItemChangesAdditionalProperty,
        )

        d = dict(src_dict)
        copy_group_rollover_result_results_item_changes = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = (
                CopyGroupRolloverResultResultsItemChangesAdditionalProperty.from_dict(prop_dict)
            )

            additional_properties[prop_name] = additional_property

        copy_group_rollover_result_results_item_changes.additional_properties = (
            additional_properties
        )
        return copy_group_rollover_result_results_item_changes

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(
        self, key: str
    ) -> "CopyGroupRolloverResultResultsItemChangesAdditionalProperty":
        return self.additional_properties[key]

    def __setitem__(
        self, key: str, value: "CopyGroupRolloverResultResultsItemChangesAdditionalProperty"
    ) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
