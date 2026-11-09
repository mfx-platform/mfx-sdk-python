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
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.copy_limit_kind import CopyLimitKind
from ..types import UNSET, Unset

T = TypeVar("T", bound="CopyStopoutReset")


@_attrs_define
class CopyStopoutReset:
    """
    Attributes:
        reason (str):
        limit (Union[Unset, CopyLimitKind]):
    """

    reason: str
    limit: Union[Unset, CopyLimitKind] = UNSET

    def to_dict(self) -> dict[str, Any]:
        reason = self.reason

        limit: Union[Unset, str] = UNSET
        if not isinstance(self.limit, Unset):
            limit = self.limit.value

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "reason": reason,
            }
        )
        if limit is not UNSET:
            field_dict["limit"] = limit

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        reason = d.pop("reason")

        _limit = d.pop("limit", UNSET)
        limit: Union[Unset, CopyLimitKind]
        if isinstance(_limit, Unset):
            limit = UNSET
        else:
            limit = CopyLimitKind(_limit)

        copy_stopout_reset = cls(
            reason=reason,
            limit=limit,
        )

        return copy_stopout_reset
