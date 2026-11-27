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
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.copy_group_rollover_result_results_item import (
        CopyGroupRolloverResultResultsItem,
    )


T = TypeVar("T", bound="CopyGroupRolloverResult")


@_attrs_define
class CopyGroupRolloverResult:
    """
    Attributes:
        group_id (UUID):
        dry_run (bool):
        fields (list[str]): The fields set
        results (list['CopyGroupRolloverResultResultsItem']): Each member of the page, in id order
        next_after (Union[None, UUID]): The last member answered when more follow; null after the last page
    """

    group_id: UUID
    dry_run: bool
    fields: list[str]
    results: list["CopyGroupRolloverResultResultsItem"]
    next_after: Union[None, UUID]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.copy_group_rollover_result_results_item import (
            CopyGroupRolloverResultResultsItem,
        )

        group_id = str(self.group_id)

        dry_run = self.dry_run

        fields = self.fields

        results = []
        for results_item_data in self.results:
            results_item = results_item_data.to_dict()
            results.append(results_item)

        next_after: Union[None, str]
        if isinstance(self.next_after, UUID):
            next_after = str(self.next_after)
        else:
            next_after = self.next_after

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "group_id": group_id,
                "dry_run": dry_run,
                "fields": fields,
                "results": results,
                "next_after": next_after,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.copy_group_rollover_result_results_item import (
            CopyGroupRolloverResultResultsItem,
        )

        d = dict(src_dict)
        group_id = UUID(d.pop("group_id"))

        dry_run = d.pop("dry_run")

        fields = cast(list[str], d.pop("fields"))

        results = []
        _results = d.pop("results")
        for results_item_data in _results:
            results_item = CopyGroupRolloverResultResultsItem.from_dict(results_item_data)

            results.append(results_item)

        def _parse_next_after(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                next_after_type_0 = UUID(data)

                return next_after_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        next_after = _parse_next_after(d.pop("next_after"))

        copy_group_rollover_result = cls(
            group_id=group_id,
            dry_run=dry_run,
            fields=fields,
            results=results,
            next_after=next_after,
        )

        copy_group_rollover_result.additional_properties = d
        return copy_group_rollover_result

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
