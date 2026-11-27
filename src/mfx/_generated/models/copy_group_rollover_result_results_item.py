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

from ..models.copy_group_rollover_result_results_item_outcome import (
    CopyGroupRolloverResultResultsItemOutcome,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.copy_group_rollover_result_results_item_changes import (
        CopyGroupRolloverResultResultsItemChanges,
    )


T = TypeVar("T", bound="CopyGroupRolloverResultResultsItem")


@_attrs_define
class CopyGroupRolloverResultResultsItem:
    """
    Attributes:
        follower_id (UUID):
        outcome (CopyGroupRolloverResultResultsItemOutcome):
        changes (CopyGroupRolloverResultResultsItemChanges): Each field changed, with its from and to; empty unless
            changed
        reason (Union[None, str]): Why it was refused, as an update of it would be; null otherwise
    """

    follower_id: UUID
    outcome: CopyGroupRolloverResultResultsItemOutcome
    changes: "CopyGroupRolloverResultResultsItemChanges"
    reason: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.copy_group_rollover_result_results_item_changes import (
            CopyGroupRolloverResultResultsItemChanges,
        )

        follower_id = str(self.follower_id)

        outcome = self.outcome.value

        changes = self.changes.to_dict()

        reason: Union[None, str]
        reason = self.reason

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "follower_id": follower_id,
                "outcome": outcome,
                "changes": changes,
                "reason": reason,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.copy_group_rollover_result_results_item_changes import (
            CopyGroupRolloverResultResultsItemChanges,
        )

        d = dict(src_dict)
        follower_id = UUID(d.pop("follower_id"))

        outcome = CopyGroupRolloverResultResultsItemOutcome._read(d.pop("outcome"))

        changes = CopyGroupRolloverResultResultsItemChanges.from_dict(d.pop("changes"))

        def _parse_reason(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        reason = _parse_reason(d.pop("reason"))

        copy_group_rollover_result_results_item = cls(
            follower_id=follower_id,
            outcome=outcome,
            changes=changes,
            reason=reason,
        )

        copy_group_rollover_result_results_item.additional_properties = d
        return copy_group_rollover_result_results_item

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
